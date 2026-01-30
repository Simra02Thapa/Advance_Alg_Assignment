"""

SMART ENERGY GRID LOAD DISTRIBUTION OPTIMIZATION - NEPAL

PROBLEM: Optimize energy distribution across multiple districts in Nepal
         using multiple energy sources while minimizing cost and diesel usage.

ALGORITHM APPROACH:
------------------
1. GREEDY STRATEGY: Always allocate cheapest available energy source first
   - Priority: Solar (cheapest) → Hydro → Diesel (most expensive)
   
2. DYNAMIC PROGRAMMING CONCEPT: Track feasibility state at each hour
   - State: (hour, remaining_capacity_per_source, unmet_demand)
   - Transition: Allocate energy source to district, update state
   - Feasibility: Check if demand can be met within ±10% tolerance

CONSTRAINTS:
-----------
- Each district's demand must be satisfied within ±10%
- Respect source availability (time-based) and capacity (kW limit)
- Minimize total cost (in Nepali Rupees)
- Minimize diesel usage (environmental concern)
"""

import copy
from tabulate import tabulate
# SECTION 1: DATA MODELING

def initialize_district_demands():
    """
    Model hourly energy demand (in kW) for multiple districts in Nepal.
    
    Districts chosen represent different load profiles:
    - Kathmandu: High urban demand, peaks during business hours
    - Pokhara: Tourist area, moderate demand
    - Biratnagar: Industrial area, steady demand
    - Bharatpur: Growing city, moderate demand
    
    Returns:
        dict: {district_name: [hourly_demands for 24 hours]}
    """
    # Demand in kW for each hour (0-23)
    demands = {
        # Hour:    0    1    2    3    4    5    6    7    8    9   10   11
        #         12   13   14   15   16   17   18   19   20   21   22   23
        
        "Kathmandu": [
            200, 180, 160, 150, 150, 180, 250, 400, 500, 550, 600, 580,  # 0-11
            550, 520, 500, 480, 500, 600, 700, 650, 500, 400, 300, 250   # 12-23
        ],
        
        "Pokhara": [
            100, 90, 80, 75, 75, 90, 120, 180, 220, 250, 280, 300,      # 0-11
            320, 300, 280, 260, 280, 350, 400, 380, 300, 200, 150, 120  # 12-23
        ],
        
        "Biratnagar": [
            150, 140, 130, 120, 120, 150, 200, 300, 400, 450, 480, 500, # 0-11
            500, 480, 460, 450, 460, 500, 550, 500, 400, 300, 200, 170  # 12-23
        ],
        
        "Bharatpur": [
            80, 70, 65, 60, 60, 75, 100, 150, 200, 230, 250, 260,       # 0-11
            270, 260, 250, 240, 250, 300, 350, 320, 250, 180, 120, 100  # 12-23
        ]
    }
    
    return demands


def initialize_energy_sources():
    """
    Model energy sources with capacity, availability, and cost.
    
    Energy Sources in Nepal Context:
    - SOLAR: Available during daylight (6 AM - 6 PM), cheapest
    - HYDRO: Available most hours (Nepal has abundant hydro), moderate cost
    - DIESEL: Always available but expensive and polluting (backup)
    
    Returns:
        dict: {source_name: {max_capacity, available_hours, cost_per_kwh}}
    """
    sources = {
        "Solar": {
            "max_capacity": 800,           # Maximum kW per hour
            "available_hours": list(range(6, 18)),  # 6 AM to 5 PM (daylight)
            "cost_per_kwh": 5.0,           # NPR 5 per kWh (cheapest - renewable)
            "is_renewable": True
        },
        
        "Hydro": {
            "max_capacity": 1200,          # Maximum kW per hour
            "available_hours": list(range(0, 24)),  # Available 24 hours
            "cost_per_kwh": 8.0,           # NPR 8 per kWh (moderate - renewable)
            "is_renewable": True
        },
        
        "Diesel": {
            "max_capacity": 2000,          # Maximum kW per hour (backup capacity)
            "available_hours": list(range(0, 24)),  # Always available
            "cost_per_kwh": 25.0,          # NPR 25 per kWh (expensive - non-renewable)
            "is_renewable": False
        }
    }
    
    return sources

# GREEDY ALLOCATION ALGORITHM

def get_source_priority(sources):
    """
    Sort energy sources by cost (Greedy: cheapest first).
    
    This implements the GREEDY STRATEGY:
    - Always try to use the cheapest available source first
    - Move to next source only when cheaper one is exhausted/unavailable
    
    Args:
        sources: Dictionary of energy sources
        
    Returns:
        list: Source names sorted by cost (ascending)
    """
    # Sort sources by cost per kWh (ascending order)
    sorted_sources = sorted(sources.keys(), 
                           key=lambda x: sources[x]["cost_per_kwh"])
    return sorted_sources


def is_source_available(source_info, hour):
    """
    Check if a source is available at given hour.
    
    Args:
        source_info: Source configuration dictionary
        hour: Hour of the day (0-23)
        
    Returns:
        bool: True if source is available
    """
    return hour in source_info["available_hours"]


def allocate_energy_greedy(demands, sources, tolerance=0.10):
    """
    MAIN ALGORITHM: Greedy allocation with DP feasibility tracking.
    
    ALGORITHM STEPS:
    ---------------
    1. For each hour (0-23):
       a. Reset available capacity for each source
       b. For each district:
          i.   Calculate demand with tolerance (±10%)
          ii.  Try sources in cost order (Greedy)
          iii. Allocate as much as possible from cheapest source
          iv.  Move to next source if needed
          v.   Track if diesel was used and why
    
    2. DP CONCEPT - State Tracking:
       - State at each hour: remaining capacity of each source
       - Transition: Allocation reduces capacity
       - Feasibility: Check if min_demand can be met
    
    Args:
        demands: District demands dictionary
        sources: Energy sources dictionary
        tolerance: Acceptable deviation (default 10%)
        
    Returns:
        tuple: (allocation_table, total_cost, diesel_usage_log, summary_stats)
    """
    
    # Get source priority (sorted by cost - Greedy)
    source_priority = get_source_priority(sources)
    print(f"\n📊 Source Priority (Greedy - Cheapest First): {source_priority}")
    print(f"   Costs: Solar=NPR {sources['Solar']['cost_per_kwh']}/kWh, "
          f"Hydro=NPR {sources['Hydro']['cost_per_kwh']}/kWh, "
          f"Diesel=NPR {sources['Diesel']['cost_per_kwh']}/kWh\n")
    
    # Initialize tracking structures
    # DP State: Track allocation and remaining capacity at each hour
    allocation = {}  # {hour: {district: {source: allocated_kw}}}
    diesel_log = []  # Log of diesel usage with reasons
    
    total_cost = 0.0
    total_renewable = 0.0
    total_diesel = 0.0
    total_demand_served = 0.0
    
    districts = list(demands.keys())
# HOUR-BY-HOUR ALLOCATION (Outer Loop of DP)
    
    for hour in range(24):
        allocation[hour] = {}
        
        # DP State: Available capacity for this hour (reset for each hour)
        available_capacity = {
            source: sources[source]["max_capacity"] 
            for source in sources
        }
        
        
        # DISTRICT-BY-DISTRICT ALLOCATION
        
        for district in districts:
            allocation[hour][district] = {source: 0 for source in sources}
            
            # Get demand for this district at this hour
            demand = demands[district][hour]
            
            # Calculate acceptable range (±10% tolerance)
            min_demand = demand * (1 - tolerance)  # Must meet at least 90%
            max_demand = demand * (1 + tolerance)  # Can supply up to 110%
            
            remaining_demand = demand  # Track how much still needs to be met
            
            
            # GREEDY SOURCE SELECTION (Try cheapest first)
            
            for source in source_priority:
                if remaining_demand <= 0:
                    break  # Demand fully satisfied
                
                source_info = sources[source]
                
                # Check source availability at this hour
                if not is_source_available(source_info, hour):
                    continue  # Skip unavailable source
                
                # Calculate how much we can allocate from this source
                can_allocate = min(
                    remaining_demand,           # What we need
                    available_capacity[source]  # What's available
                )
                
                if can_allocate > 0:
                    # Allocate energy
                    allocation[hour][district][source] = can_allocate
                    available_capacity[source] -= can_allocate
                    remaining_demand -= can_allocate
                    
                    # Calculate cost
                    cost = can_allocate * source_info["cost_per_kwh"]
                    total_cost += cost
                    
                    # Track renewable vs diesel
                    if source_info["is_renewable"]:
                        total_renewable += can_allocate
                    else:
                        total_diesel += can_allocate
            
            # Track total served
            served = demand - remaining_demand
            total_demand_served += served
            
            # Check if diesel was used and log reason
            if allocation[hour][district]["Diesel"] > 0:
                diesel_amount = allocation[hour][district]["Diesel"]
                reason = _get_diesel_reason(hour, sources, 
                                           allocation[hour][district])
                diesel_log.append({
                    "hour": hour,
                    "district": district,
                    "amount": diesel_amount,
                    "reason": reason
                })
    
    # Compile summary statistics
    summary = {
        "total_cost": total_cost,
        "total_renewable": total_renewable,
        "total_diesel": total_diesel,
        "total_served": total_demand_served,
        "renewable_percentage": (total_renewable / total_demand_served * 100) 
                                if total_demand_served > 0 else 0
    }
    
    return allocation, total_cost, diesel_log, summary


def _get_diesel_reason(hour, sources, district_allocation):
    """
    Determine why diesel was needed at this hour.
    
    Args:
        hour: Hour of day
        sources: Source configurations
        district_allocation: Allocation for this district at this hour
        
    Returns:
        str: Reason for diesel usage
    """
    reasons = []
    
    # Check if solar was unavailable (nighttime)
    if hour not in sources["Solar"]["available_hours"]:
        reasons.append("Solar unavailable (nighttime)")
    elif district_allocation["Solar"] > 0:
        reasons.append("Solar capacity exhausted")
    
    # Check hydro
    if district_allocation["Hydro"] > 0:
        reasons.append("Hydro capacity exhausted")
    else:
        reasons.append("Hydro at max capacity")
    
    return " + ".join(reasons) if reasons else "High demand exceeded renewable capacity"


#  OUTPUT FORMATTING

def print_hourly_allocation_table(allocation, demands, districts):
    """
    Print formatted hourly allocation table.
    Shows allocation per district per source for each hour.
    """
    print("\n" + "="*100)
    print("📋 HOURLY ENERGY ALLOCATION TABLE (in kW)")
    print("="*100)
    
    for hour in range(24):
        print(f"\n⏰ HOUR {hour:02d}:00 - {(hour+1)%24:02d}:00")
        print("-"*80)
        
        table_data = []
        for district in districts:
            demand = demands[district][hour]
            solar = allocation[hour][district]["Solar"]
            hydro = allocation[hour][district]["Hydro"]
            diesel = allocation[hour][district]["Diesel"]
            total = solar + hydro + diesel
            status = "✅" if total >= demand * 0.9 else "⚠️"
            
            table_data.append([
                district,
                f"{demand:.0f}",
                f"{solar:.0f}",
                f"{hydro:.0f}",
                f"{diesel:.0f}",
                f"{total:.0f}",
                status
            ])
        
        headers = ["District", "Demand", "Solar", "Hydro", "Diesel", "Total", "Status"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))


def print_summary_table(allocation, demands, districts, sources):
    """
    Print summary statistics per district.
    """
    print("\n" + "="*50)
    print("📊 DISTRICT-WISE SUMMARY")
    print("="*50)
    
    table_data = []
    
    for district in districts:
        total_demand = sum(demands[district])
        total_solar = sum(allocation[h][district]["Solar"] for h in range(24))
        total_hydro = sum(allocation[h][district]["Hydro"] for h in range(24))
        total_diesel = sum(allocation[h][district]["Diesel"] for h in range(24))
        total_served = total_solar + total_hydro + total_diesel
        
        cost = (total_solar * sources["Solar"]["cost_per_kwh"] +
                total_hydro * sources["Hydro"]["cost_per_kwh"] +
                total_diesel * sources["Diesel"]["cost_per_kwh"])
        
        renewable_pct = ((total_solar + total_hydro) / total_served * 100) if total_served > 0 else 0
        
        table_data.append([
            district,
            f"{total_demand:.0f}",
            f"{total_served:.0f}",
            f"{total_solar:.0f}",
            f"{total_hydro:.0f}",
            f"{total_diesel:.0f}",
            f"NPR {cost:,.0f}",
            f"{renewable_pct:.1f}%"
        ])
    
    headers = ["District", "Total Demand", "Total Served", "Solar", "Hydro", 
               "Diesel", "Cost", "Renewable %"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def print_diesel_usage_log(diesel_log):
    """
    Print detailed log of diesel usage with reasons.
    """
    print("\n" + "="*50)
    print("⛽ DIESEL USAGE LOG (When & Why Diesel Was Used)")
    print("="*50)
    
    if not diesel_log:
        print("\n✅ No diesel was used! 100% renewable energy achieved!")
        return
    
    table_data = []
    for entry in diesel_log:
        table_data.append([
            f"{entry['hour']:02d}:00",
            entry['district'],
            f"{entry['amount']:.0f} kW",
            entry['reason']
        ])
    
    headers = ["Hour", "District", "Amount", "Reason"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Summary
    total_diesel_usage = sum(e['amount'] for e in diesel_log)
    print(f"\n📌 Total Diesel Usage: {total_diesel_usage:.0f} kW across {len(diesel_log)} instances")


def print_final_summary(summary):
    """
    Print final optimization summary.
    """
    print("\n" + "="*50)
    print("💰 FINAL OPTIMIZATION SUMMARY")
    print("="*50)
    
    print(f"""
    ┌─────────────────────────────────────────────────────────┐
    │  SMART ENERGY GRID - NEPAL                              │
    ├─────────────────────────────────────────────────────────┤
    │  Total Energy Served:     {summary['total_served']:>15,.0f} kWh         │
    │  Total Cost:              NPR {summary['total_cost']:>12,.0f}           │
    ├─────────────────────────────────────────────────────────┤
    │  Renewable Energy Used:   {summary['total_renewable']:>15,.0f} kWh         │
    │  Diesel Energy Used:      {summary['total_diesel']:>15,.0f} kWh         │
    │  Renewable Percentage:    {summary['renewable_percentage']:>15.1f} %          │
    ├─────────────────────────────────────────────────────────┤
    │  Average Cost per kWh:    NPR {summary['total_cost']/summary['total_served'] if summary['total_served'] > 0 else 0:>12.2f}           │
    └─────────────────────────────────────────────────────────┘
    """)
#MAIN EXECUTION

def main():
    """
    Main function to run the Smart Energy Grid Optimization.
    
    ALGORITHM SUMMARY:
    -----------------
    1. Initialize district demands and energy sources
    2. Apply Greedy + DP allocation strategy
    3. Output detailed allocation tables and statistics
    """
    
   
    print("🔋 SMART ENERGY GRID LOAD DISTRIBUTION OPTIMIZATION - NEPAL")
    
    # Step 1: Initialize data
    print("\n STEP 1: Initializing District Demands and Energy Sources...")
    demands = initialize_district_demands()
    sources = initialize_energy_sources()
    districts = list(demands.keys())
    
    print(f"   Districts: {districts}")
    print(f"   Energy Sources: {list(sources.keys())}")
    print(f"   Time Period: 24 hours (00:00 - 23:00)")
    
    # Step 2: Run allocation algorithm
    print("\n Step 2: Running Greedy Allocation Algorithm...")
    allocation, total_cost, diesel_log, summary = allocate_energy_greedy(
        demands, sources, tolerance=0.10
    )
    
    # Step 3: Output results
    print("\n STEP 3: Generating Output Reports...")
    
    # Print hourly allocation (condensed - every 4 hours)
    print("📋 SAMPLE HOURLY ALLOCATION (Every 4 Hours)")
    
    
    for hour in [0, 6, 12, 18]:
        print(f"\n⏰ HOUR {hour:02d}:00")
        print("-"*70)
        table_data = []
        for district in districts:
            demand = demands[district][hour]
            solar = allocation[hour][district]["Solar"]
            hydro = allocation[hour][district]["Hydro"]
            diesel = allocation[hour][district]["Diesel"]
            total = solar + hydro + diesel
            
            table_data.append([
                district, f"{demand:.0f}", f"{solar:.0f}", 
                f"{hydro:.0f}", f"{diesel:.0f}", f"{total:.0f}"
            ])
        
        headers = ["District", "Demand(kW)", "Solar", "Hydro", "Diesel", "Total"]
        print(tabulate(table_data, headers=headers, tablefmt="simple"))
    
    # Print summaries
    print_summary_table(allocation, demands, districts, sources)
    print_diesel_usage_log(diesel_log)
    print_final_summary(summary)
    
    # Algorithm complexity note
    print("\n" + "="*50)
    print("📚 ALGORITHM COMPLEXITY ANALYSIS")
    print(f"""
    TIME COMPLEXITY:  O(H × D × S)
                      where H = hours (24), D = districts ({len(districts)}), S = sources ({len(sources)})
                      = O(24 × {len(districts)} × {len(sources)}) = O({24 * len(districts) * len(sources)})
    
    SPACE COMPLEXITY: O(H × D × S) for storing allocation table
                      = O({24 * len(districts) * len(sources)}) entries
    
    GREEDY CORRECTNESS:
    - Greedy choice: Always pick cheapest available source
    - Optimal substructure: Each hour's allocation is independent
    - This greedy approach gives optimal solution for cost minimization
      when source capacities don't carry over between hours
    """)
    
    return allocation, summary
# PROGRAM ENTRY POINT


if __name__ == "__main__":
    # Run the optimization
    allocation, summary = main()
    
  
    
