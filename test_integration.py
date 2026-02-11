#!/usr/bin/env python3
"""
Simple test script to verify OMIE data fetching and price calculation.
Run this before installing in Home Assistant to verify dependencies work.
"""

import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

try:
    from omie_data import get_omie_data
    import pandas as pd
    print("[OK] Dependencies imported successfully")
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("Install with: pip install omie-market-data pandas openpyxl")
    sys.exit(1)

LISBON_TZ = ZoneInfo("Europe/Lisbon")


def test_omie_connection():
    """Test fetching OMIE data."""
    print("\n=== Testing OMIE Connection ===")
    try:
        today = date.today()
        date_dt = datetime.combine(today, datetime.min.time())
        df = get_omie_data(date_dt)
        
        if df is None or df.empty:
            print(f"[WARNING] No data returned for {today}")
            return False
        
        print(f"[OK] Successfully fetched OMIE data for {today}")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        
        # Check for Portuguese price column
        price_cols = [col for col in df.columns if 'portugal' in col.lower() or 'portug' in col.lower()]
        if price_cols:
            print(f"[OK] Found Portuguese price column: {price_cols[0]}")
            print(f"  Sample price: {df[price_cols[0]].iloc[0]} EUR/MWh")
        else:
            print("[WARNING] Could not find Portuguese price column")
            print(f"  Available columns: {list(df.columns)}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error fetching OMIE data: {e}")
        return False


def test_loss_profile():
    """Test loading loss profile Excel file."""
    print("\n=== Testing Loss Profile ===")
    try:
        import os
        from pathlib import Path
        
        profile_path = Path(__file__).parent / "custom_components" / "coopernico" / "perfil_perda_2026.xlsx"
        
        if not profile_path.exists():
            print(f"[WARNING] Loss profile file not found at: {profile_path}")
            return False
        
        print(f"[OK] Loss profile file found: {profile_path}")
        
        excel_data = pd.read_excel(profile_path)
        print(f"[OK] Successfully loaded Excel file")
        print(f"  Rows: {len(excel_data)}")
        print(f"  Columns: {list(excel_data.columns)}")
        
        # Check for required columns
        required_cols = ['Data', 'Hora', 'BT']
        missing_cols = [col for col in required_cols if col not in excel_data.columns]
        if missing_cols:
            print(f"[WARNING] Missing required columns: {missing_cols}")
            return False
        
        print(f"[OK] All required columns present")
        print(f"  Sample BT value: {excel_data['BT'].iloc[0]}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error loading loss profile: {e}")
        return False


def test_price_calculation():
    """Test price calculation logic."""
    print("\n=== Testing Price Calculation ===")
    try:
        margin_k = 0.009
        go_value = 0.001
        omie_price = 0.05  # Example: 50 EUR/MWh = 0.05 €/kWh
        loss_factor = 0.02  # Example: 2% loss
        
        coopernico_price = (omie_price + margin_k) * (1 + loss_factor) + go_value
        expected = (0.05 + 0.009) * 1.02 + 0.001
        expected = round(expected, 4)
        
        print(f"[OK] Price calculation test:")
        print(f"  OMIE Price: {omie_price} €/kWh")
        print(f"  Margin: {margin_k} €/kWh")
        print(f"  Loss Factor: {loss_factor}")
        print(f"  GO Value: {go_value} €/kWh")
        print(f"  Coopernico Price: {coopernico_price:.4f} €/kWh")
        print(f"  Expected: {expected:.4f} €/kWh")
        
        if abs(coopernico_price - expected) < 0.0001:
            print("[OK] Calculation matches expected result")
            return True
        else:
            print("[WARNING] Calculation does not match expected result")
            return False
    except Exception as e:
        print(f"[ERROR] Error in price calculation: {e}")
        return False


def main():
    """Run all tests."""
    print("Coopernico Integration Test Script")
    print("=" * 50)
    
    results = []
    
    # Test dependencies
    print("\n=== Testing Dependencies ===")
    try:
        import pandas as pd
        import openpyxl
        from omie_data import get_omie_data
        print("[OK] All dependencies available")
        results.append(True)
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e}")
        results.append(False)
        return
    
    # Run tests
    results.append(test_omie_connection())
    results.append(test_loss_profile())
    results.append(test_price_calculation())
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if all(results):
        print("\n[SUCCESS] All tests passed! Integration should work in Home Assistant.")
        return 0
    else:
        print("\n[WARNING] Some tests failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
