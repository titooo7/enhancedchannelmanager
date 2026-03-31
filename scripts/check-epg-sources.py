import asyncio
import os
import sys

# Add backend to path so we can import modules
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from dispatcharr_client import get_client

async def list_sources():
    client = get_client()
    print("\n--- Fetching EPG Sources from Dispatcharr ---")
    try:
        # 1. Try to get explicit sources list
        sources = await client.get_epg_sources()
        if sources:
            print(f"{'ID':<10} | {'Name'}")
            print("-" * 30)
            for s in sources:
                print(f"{s.get('id', '??'):<10} | {s.get('name', 'Unknown')}")
        else:
            print("No explicit sources returned by API.")
            
        # 2. Also check the grid metadata for what's actually being used today
        print("\n--- Sources discovered in today's EPG Grid ---")
        grid = await client.get_epg_grid()
        channels = grid.get("channels", [])
        discovered_ids = set()
        for ch in channels:
            sid = ch.get("epg_source") or ch.get("epg_source_id")
            if sid:
                discovered_ids.add(sid)
        
        if discovered_ids:
            print(f"Source IDs present in grid: {sorted(list(discovered_ids))}")
        else:
            print("No source IDs found in grid metadata.")
            
    except Exception as e:
        print(f"Error: {e}")
    print("\n--------------------------------------------\n")

if __name__ == "__main__":
    asyncio.run(list_sources())
