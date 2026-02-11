"""OMIE client for fetching and calculating Coopernico prices."""
from __future__ import annotations

import os
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
from omie_data import get_omie_data

LISBON_TZ = ZoneInfo("Europe/Lisbon")


def _get_loss_profile_path() -> Path:
    """Get the path to the bundled loss profile Excel file."""
    return Path(__file__).parent / "perfil_perda_2026.xlsx"


def _load_loss_profile() -> pd.DataFrame | None:
    """Load the loss profile from the bundled Excel file."""
    profile_path = _get_loss_profile_path()
    if not profile_path.exists():
        return None

    try:
        excel_data = pd.read_excel(profile_path)
        data = pd.DataFrame(
            excel_data, columns=["Data", "Hora", "BT", "MT", "AT", "AT/RT"]
        )

        # Parse datetime from Data and Hora columns
        def get_datetime_perfis(x):
            date_format = "%Y-%m-%d - %H:%M"
            data_only = str(x["Data"]).split(" ")[0]
            if "24" in str(x["Hora"]):
                day_helper = datetime.strptime(data_only + " - 00:00", date_format)
                day_helper += timedelta(days=1)
                return day_helper
            else:
                date_str = data_only + " - " + str(x["Hora"])
            return datetime.strptime(date_str, date_format)

        data["datetime"] = data.apply(get_datetime_perfis, axis=1)
        return data
    except Exception:
        return None


def _get_portuguese_price_column(df: pd.DataFrame) -> str | None:
    """Return the column name for Portuguese marginal price (EUR/MWh), or None."""
    for col in df.columns:
        col_lower = col.lower()
        # Prefer: marginal price for Portugal (not import/export or power)
        if ("marginal" in col_lower or "precio" in col_lower) and (
            "portugus" in col_lower
            or "portugal" in col_lower
            or "portugués" in col_lower
        ):
            return col
    for col in df.columns:
        col_lower = col.lower()
        if "portugal" in col_lower or ("pt" in col_lower and "price" in col_lower):
            return col
    for col in df.columns:
        col_lower = col.lower()
        if "price" in col_lower and "start" not in col_lower and "end" not in col_lower:
            return col
    return None


class CoopernicoOMIEClient:
    """Client for fetching OMIE data and calculating Coopernico prices."""

    def __init__(
        self,
        margin_k: float = 0.009,
        go_value: float = 0.001,
        tarifa: str = "SIMPLES",
        diario: bool = True,
        go_enabled: bool = False,
    ) -> None:
        """Initialize the client."""
        self.margin_k = margin_k  # Coopernico margin €/kWh
        self.go_value = go_value if go_enabled else 0.0  # Guarantees of Origin €/kWh
        self.tarifa = tarifa
        self.diario = diario

    def fetch_omie_marginal_prices(
        self, date_ini: date, date_end: date
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Fetch OMIE marginal price data for the given date range.
        Returns (raw_omie_df, price_df):
          - raw_omie_df: Raw library DataFrame with start_period and Portuguese price column in EUR/MWh.
          - price_df: DataFrame with datetime and price in €/kWh.
        """
        all_data = []
        current_date = date_ini

        while current_date <= date_end:
            date_dt = datetime.combine(current_date, datetime.min.time())
            df_day = get_omie_data(date_dt)

            if df_day is not None and not df_day.empty:
                all_data.append(df_day)

            current_date += timedelta(days=1)

        if not all_data:
            return pd.DataFrame(), pd.DataFrame()

        combined_df = pd.concat(all_data, ignore_index=True)

        # Convert start_period to Portuguese timezone (Europe/Lisbon)
        start_period_series = pd.to_datetime(combined_df["start_period"])
        if start_period_series.dt.tz is None:
            start_period_pt = start_period_series.dt.tz_localize(LISBON_TZ)
        else:
            start_period_pt = start_period_series.dt.tz_convert(LISBON_TZ)
        combined_df["start_period"] = start_period_pt
        combined_df["datetime"] = combined_df["start_period"]

        price_col = _get_portuguese_price_column(combined_df)
        if price_col is None:
            return pd.DataFrame(), combined_df

        # Convert EUR/MWh to €/kWh and create price dataframe
        price_df = pd.DataFrame(
            {
                "datetime": combined_df["datetime"],
                "price_omie": combined_df[price_col] / 1000.0,  # Convert to €/kWh
            }
        )

        raw_omie_df = combined_df[["start_period", price_col]].copy()
        return raw_omie_df, price_df

    def calculate_coopernico_price(
        self, omie_price: float, loss_factor: float = 0.0
    ) -> float:
        """
        Calculate Coopernico price from OMIE price.
        Formula: (OMIE + margin) * (1 + loss_factor)
        """
        return (omie_price + self.margin_k) * (1 + loss_factor) + self.go_value

    def fetch_and_calculate_prices(
        self, date_ini: date, date_end: date
    ) -> dict:
        """
        Fetch OMIE prices and calculate Coopernico prices using loss profile.
        Returns a dictionary with current and future prices.
        """
        raw_omie_df, price_df = self.fetch_omie_marginal_prices(date_ini, date_end)

        if price_df.empty:
            return {}

        # Load loss profile from bundled Excel file
        loss_profile_df = _load_loss_profile()
        
        if loss_profile_df is not None and not loss_profile_df.empty:
            # Filter loss profile to date range
            dt_max = datetime.combine(date_end, datetime.max.time())
            dt_min = datetime.combine(date_ini, datetime.min.time())
            loss_profile_filtered = loss_profile_df.loc[
                (loss_profile_df["datetime"] < dt_max)
                & (loss_profile_df["datetime"] > dt_min)
            ].copy()

            if not loss_profile_filtered.empty:
                # Create merge keys for both dataframes (15-minute intervals)
                price_df["merge_key"] = pd.to_datetime(price_df["datetime"]).dt.floor(
                    "15min"
                )
                loss_profile_filtered["merge_key"] = pd.to_datetime(
                    loss_profile_filtered["datetime"]
                ).dt.floor("15min")

                # Merge loss profile with OMIE price data (left join from loss profile)
                merged_df = loss_profile_filtered.merge(
                    price_df[["merge_key", "price_omie"]],
                    on="merge_key",
                    how="left",
                )
                
                # Only keep rows with both OMIE and loss profile data
                merged_df = merged_df.dropna(subset=["price_omie"])
                
                # Filter to available OMIE data range (use datetime from loss profile)
                available_end = price_df["merge_key"].max()
                merged_df = merged_df[merged_df["datetime"] <= available_end]

                if not merged_df.empty:
                    # Calculate Coopernico prices with loss factor: (OMIE + margin) * (1 + BT)
                    merged_df["price_coopernico"] = (
                        merged_df["price_omie"] + self.margin_k
                    ) * (1 + merged_df["BT"]) + self.go_value
                    
                    # Use the merged dataframe with datetime from loss profile
                    price_df = merged_df[["datetime", "price_omie", "price_coopernico"]].copy()
                else:
                    # No matching data, use default
                    price_df["price_coopernico"] = price_df["price_omie"].apply(
                        lambda x: self.calculate_coopernico_price(x, 0.0)
                    )
            else:
                # No loss profile data for date range, use default
                price_df["price_coopernico"] = price_df["price_omie"].apply(
                    lambda x: self.calculate_coopernico_price(x, 0.0)
                )
        else:
            # No loss profile file available, use default
            price_df["price_coopernico"] = price_df["price_omie"].apply(
                lambda x: self.calculate_coopernico_price(x, 0.0)
            )

        # Get current price
        now = datetime.now(LISBON_TZ)
        current_prices = price_df[price_df["datetime"] <= now]
        current_price = (
            current_prices.iloc[-1]["price_coopernico"]
            if not current_prices.empty
            else None
        )

        # Get hourly prices for today and tomorrow
        price_df["date"] = price_df["datetime"].dt.date
        price_df["hour"] = price_df["datetime"].dt.hour

        today = date.today()
        tomorrow = today + timedelta(days=1)

        today_prices = price_df[price_df["date"] == today].copy()
        tomorrow_prices = price_df[price_df["date"] == tomorrow].copy()

        # Group by hour and get average
        hourly_today = (
            today_prices.groupby("hour")["price_coopernico"].mean().to_dict()
        )
        hourly_tomorrow = (
            tomorrow_prices.groupby("hour")["price_coopernico"].mean().to_dict()
        )

        # Get 15-minute interval prices for today and tomorrow
        price_df_15min = price_df.copy()
        price_df_15min["date"] = price_df_15min["datetime"].dt.date
        price_df_15min["hour"] = price_df_15min["datetime"].dt.hour
        price_df_15min["minute"] = price_df_15min["datetime"].dt.minute
        
        today_15min = price_df_15min[price_df_15min["date"] == today].copy()
        tomorrow_15min = price_df_15min[price_df_15min["date"] == tomorrow].copy()

        # Create 15-minute interval data structure
        def create_15min_dict(df_15min):
            """Create a dict with 15-minute interval prices."""
            result = {}
            for _, row in df_15min.iterrows():
                hour = int(row["hour"])
                minute = int(row["minute"])
                # Round minute to nearest 15-minute interval (0, 15, 30, 45)
                minute_rounded = (minute // 15) * 15
                key = f"H{hour:02d}M{minute_rounded:02d}"
                result[key] = float(row["price_coopernico"])
            return result

        interval_15min_today = create_15min_dict(today_15min)
        interval_15min_tomorrow = create_15min_dict(tomorrow_15min)

        return {
            "current_price": current_price,
            "current_datetime": now.isoformat(),
            "hourly_today": {f"H{h:02d}": hourly_today.get(h) for h in range(24)},
            "hourly_tomorrow": {
                f"H{h:02d}": hourly_tomorrow.get(h) for h in range(24)
            },
            "interval_15min_today": interval_15min_today,
            "interval_15min_tomorrow": interval_15min_tomorrow,
            "daily_average_today": today_prices["price_coopernico"].mean()
            if not today_prices.empty
            else None,
            "daily_average_tomorrow": tomorrow_prices["price_coopernico"].mean()
            if not tomorrow_prices.empty
            else None,
            "last_update": datetime.now(LISBON_TZ).isoformat(),
        }
