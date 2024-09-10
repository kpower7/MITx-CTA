import random

def print_status(budget, inventory, holding_charge_rate):
    print("\n--------------------------------------------------")
    print("Current Budget: ${}".format(budget))
    print("Current Inventory: {}".format(inventory))
    print("Holding Charge per Unit: ${}".format(holding_charge_rate))
    print("--------------------------------------------------\n")


def buy_materials(budget, material_price, procurement_cost):
    print("\nProcurement Phase")
    print("-----------------")
    print("Material price per unit: ${}".format(material_price))
    print("Procurement cost per order: ${}".format(procurement_cost))
    
    while True:
        try:
            quantity = int(input("Enter quantity to buy (0 to skip buying): "))
            cost = quantity * material_price + (procurement_cost if quantity > 0 else 0)
            if cost <= budget:
                return quantity, cost
            else:
                print("Not enough budget to buy {} units. Try a smaller quantity.".format(quantity))
        except ValueError:
            print("Please enter a valid integer.")



def sell_materials(inventory, sales_price, actual_demand):
    print("\nSales Phase")
    print("-----------")
    print("Market condition: ", end="")
    if sales_price > material_price:
        print("Market Boom!")
    else:
        print("Market Downturn!")
    print("Sales price per unit: ${}".format(sales_price))
    print("Actual demand: {}".format(actual_demand))

    while True:
        try:
            quantity = int(input("Enter quantity to sell (max {}): ".format(min(inventory, actual_demand))))
            if 0 <= quantity <= min(inventory, actual_demand):
                return quantity, quantity * sales_price
            else:
                print(f"Cannot sell {quantity} units. Please enter a number between 0 and {min(inventory, actual_demand)}")
        except ValueError:
            print("Please enter a valid integer.")

def calculate_holding_charge(inventory, holding_charge_rate):
    return inventory * holding_charge_rate

def get_difficulty_level():
    print("\nChoose Difficulty Level")
    print("-----------------------")
    print("1. Easy\n2. Medium\n3. Hard")
    choice = input("Select (1-3): ")
    if choice == '1':
        print("Difficulty set to Easy.")
        return 0.5
    elif choice == '2':
        print("Difficulty set to Medium.")
        return 1
    elif choice == '3':
        print("Difficulty set to Hard.")
        return 2
    else:
        print("Invalid choice. Defaulting to Medium.")
        return 1

def round_variation(base_value, variation_factor):
    """Calculates a varied value based on a base value and a variation factor."""
    return int(base_value * random.uniform(1 - variation_factor, 1 + variation_factor))

def determine_sales_price(material_price, difficulty_level):
    downturn_chance = 0.2 + 0.025 * difficulty_level  # Adjusted for more variability
    if random.random() < downturn_chance:
        return round_variation(material_price * random.uniform(0.8, 1), 0.1)  # Less frequent below cost
    else:
        return round_variation(material_price * random.uniform(1.1, 1.6), 0.1)  # Higher potential profits

def generate_forecasted_demands(base_demand, variation_factor, rounds):
    return [round_variation(base_demand, variation_factor) for _ in range(rounds)]


# Game Start
print("Welcome to the Supply Chain Management Game!")
print("In this game, your goal is to manage procurement and sales to maximize profit.")
print("Each round, you will decide how much inventory to purchase, considering:")
print("  - Demand is randomly variable, adding an element of uncertainty.")
print("  - The procurement cost per order is fixed and does not change.")
print("  - Holding inventory incurs a charge, so manage your inventory wisely.")
print("  - Any inventory left over at the end of the game will incur a holding fee,")
print("    and you will lose the potential sales price, affecting your final profit.")
print("Market conditions can vary, so plan your strategy carefully to end the game")
print("with the highest possible profit. Let's get started!\n")

# Initial game setup
starting_budget = budget = 10000
inventory = 0
rounds = 5
holding_charge_rate = get_difficulty_level()
procurement_cost = 200  # Define procurement cost here
total_procurement_cost = 0
total_sales_revenue = 0
total_holding_charge = 0

# Consistent variation parameters
base_material_price = 20
base_sales_price = 35
base_demand = 100
variation_factor = 0.2
forecasted_demands = generate_forecasted_demands(base_demand, variation_factor, rounds)


for round in range(1, rounds + 1):
    print("\nRound {} ({} rounds total)".format(round, rounds))

    # Apply holding charge
    if round > 1:
        holding_charge = calculate_holding_charge(inventory, holding_charge_rate)
        budget -= holding_charge
        total_holding_charge += holding_charge
        print("Holding charge for carried over inventory: ${}".format(holding_charge))

    print_status(budget, inventory, holding_charge_rate)

    # Display forecasted demand for all remaining rounds
    print("Forecasted demand for upcoming rounds:")
    for i in range(round - 1, rounds):
        print("Round {}: {}".format(i + 1, forecasted_demands[i]))

    # Procurement phase
    material_price = round_variation(base_material_price, variation_factor)
    forecasted_demand = forecasted_demands[round - 1]  # Use the pre-generated forecasted demand

    quantity_bought, cost = buy_materials(budget, material_price, procurement_cost)
    budget -= cost
    inventory += quantity_bought
    total_procurement_cost += cost

    # Sales phase with adjusted market downturn frequency
    sales_price = determine_sales_price(material_price, holding_charge_rate)
    actual_demand = max(0, int(forecasted_demand * random.uniform(0.75, 1.25)))
    quantity_sold, revenue = sell_materials(inventory, sales_price, actual_demand)
    budget += revenue
    inventory -= quantity_sold
    total_sales_revenue += revenue


    print_status(budget, inventory, holding_charge_rate)

#End of Game
print("\nEnd of Game")
print("-----------")

# Calculate final holding charge for leftover inventory
final_holding_charge = calculate_holding_charge(inventory, holding_charge_rate)
budget -= final_holding_charge
total_holding_charge += final_holding_charge  

final_profit = budget - starting_budget

if inventory > 0:
    print(f"Final holding charge for leftover inventory: ${final_holding_charge}")
    print(f"Inventory left over: {inventory} units")
    ending_inventory_value = inventory * material_price
    print(f"Ending Inventory Value: ${ending_inventory_value}")

if final_profit > 0:
    print(f"Congratulations! You made a profit of ${final_profit}!")
else:
    print(f"Better luck next time! You incurred a loss of ${-final_profit}.")


#financial summary
print("\nFinancial Summary")
print("-----------------")
print(f"Starting Budget: ${starting_budget}")
print(f"Total Procurement Cost: ${total_procurement_cost}")
print(f"Total Sales Revenue: ${total_sales_revenue}")
print(f"Total Holding Charges: ${total_holding_charge}")
print(f"Final Budget: ${budget}")
net_profit = budget - starting_budget
print(f"Net Profit/Loss: ${net_profit}")