
import unittest
import sys
import random

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount):
        if cashier.num_orders % 10 == 0 and cashier.num_orders > 0:
            if cashier.lucky_draw:
                self.wallet += 10
        self.wallet = self.wallet - amount
        cashier.receive_payment(stall, amount)

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory
        self.num_orders = 0
    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    def lucky_draw(self):
        random_number = 0
        if self.num_orders % 10 == 0:
            random_number = random.randint(1, 20)
            if random_number == 1:
                return True
            else:
                return False
        else:
            return False
        return False

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        self.num_orders += 1
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:
    def __init__(self, name, inventory, cost=7, earnings=0):
        self.name = name
        self.inventory = inventory
        self.cost = cost
        self.earnings = earnings

    def process_order(self, name, quantity):
        if self.has_item(name, quantity):
            self.earnings += self.compute_cost(quantity)
            self.inventory[name] -= quantity
        else:
            self.stock_up(name, quantity)

    def has_item(self, food_name, quantity):
        for item in self.inventory:
            if item == food_name:
                if self.inventory[food_name] >= quantity:
                    return True
        return False

    def stock_up(self, food_name, quantity):
        if food_name in self.inventory:
            self.inventory[food_name] += quantity
        else:
            self.inventory[food_name] = quantity

    def compute_cost(self, quantity):
        return self.cost * quantity

    def __str__(self):
        return "Hello, we are " + self.name + ". This is the current menu " + str(self.inventory) + ". We charge " + self.cost + " per item. We have " + self.earnings + " in total."

class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #cost computation test case was incorrect
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases
        inventory = {"Burger": 10, "Banana": 20, "Split": 15}
        s4 = Stall("Banana Booth", inventory, cost = 3)

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertFalse(s4.has_item("Apple", 10))
        self.assertFalse(s4.has_item("Apple", 0))
        # Test case 2: the stall does not have enough food item: 
        self.assertFalse(s4.has_item("Banana", 30))
        self.assertFalse(s4.has_item("Burgers", 30))
        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertTrue(s4.has_item("Burger", 9))
        self.assertTrue(s4.has_item("Burger", 10))
        self.assertTrue(s4.has_item("Burger", 0))

	# Test validate order
    def test_validate_order(self):
        # create inventories, stalls, and cashiers for testing
        inventory = {"Burger": 3, "Fruit": 10, "Split": 15}
        inventory2 = {"Zach": 3, "James": 10, "Jessica": 15}
        customer5 = Customer("Zach", 1)
        customer6 = Customer("Second", 1000)
        stall5 = Stall("Ban + Burg", inventory, 100)
        stall6 = Stall("Ban + Burger", inventory2, 100)
        cashier5 = Cashier("B&B")
        cashier5.add_stall(stall5)
        
		# case 1: test if a customer doesn't have enough money in their wallet to order
        # nothing should happen to wallet
        # nothing should happen to inventory
        self.assertEqual(customer5.wallet, 1)
        self.assertEqual(stall5.inventory["Burger"], 3)
        customer5.validate_order(cashier5, stall5, "Burger", 3)
        self.assertEqual(stall5.inventory["Burger"], 3)
        self.assertEqual(customer5.wallet, 1)
       
		# case 2: test if the stall doesn't have enough food left in stock
        # nothing should happen to wallet
        # nothing should happen to inventory
        self.assertEqual(customer5.wallet, 1)
        self.assertEqual(stall5.inventory["Burger"], 3)
        customer5.validate_order(cashier5, stall5, "Burger", 80)
        self.assertEqual(customer5.wallet, 1)
        self.assertEqual(stall5.inventory["Burger"], 3)

		# case 3: check if the cashier can order item from that stall
        # customer cannot order from this stall, and thus
        # wallet should not be effected
        # inventory should not be effected 
        self.assertEqual(customer5.wallet, 1)
        self.assertEqual(stall5.inventory["Burger"], 3)
        customer5.validate_order(cashier5, stall6, "Cheese", 1)
        self.assertEqual(stall5.inventory["Burger"], 3)
        self.assertEqual(customer5.wallet, 1)

        # case 4: valid case, customer can order and does
        # wallet should be effected, decrese by a specific amount
        # inventory should be affected for the given item, decrease by order size
        self.assertEqual(customer6.wallet, 1000)
        self.assertEqual(stall5.inventory["Burger"], 3)
        customer6.validate_order(cashier5, stall5, "Burger", 3)
        self.assertNotEqual(customer6.wallet, 1000)
        self.assertEqual(stall5.inventory["Burger"], 0)
        self.assertEqual(customer6.wallet, 700)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        customer5 = Customer("Zach", 1)
        self.assertEqual(customer5.wallet, 1)
        #adding some money
        customer5.reload_money(10)
        self.assertEqual(customer5.wallet, 11)
        #adding no money
        customer5.reload_money(0)
        self.assertEqual(customer5.wallet, 11)
    
### Write main function
def main():
    #Create different objects 
    inventory1 = {"Cheese": 2, "Tomato": 5, "Lettuce": 888}
    inventory2 = {"Lamb": 10, "Steak": 11, "Fish": 2}
    customerA = Customer("Zach", 10)
    customerB = Customer("Josh", 80)
    customerC = Customer("Anna", 40)
    stallA = Stall("AA", inventory1, 50)
    stallB = Stall("BB", inventory2, 30)
    stallC = Stall("CC", inventory2, 80)
    cashierA = Cashier("First")
    cashierA.add_stall(stallA)
    cashierA.add_stall(stallB)
    cashierB = Cashier("Second")
    cashierB.add_stall(stallA)
    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases

    #case 1: the cashier does not have the stall 
    customerA.validate_order(cashierA, stallC, "Banana", 3)
    customerB.validate_order(cashierB, stallB, "Beef", 100)
    customerC.validate_order(cashierB, stallC, "Paper", 1)
    #case 2: the casher has the stall, but not enough ordered food or the ordered food item
    customerA.validate_order(cashierA, stallB, "Lamb", 100)
    customerB.validate_order(cashierB, stallA, "Onion", 3)
    customerC.validate_order(cashierB, stallA, "Tomato", 6)
    #case 3: the customer does not have enough money to pay for the order: 
    customerA.validate_order(cashierA, stallB, "Lamb", 8)
    customerB.validate_order(cashierA, stallB, "Lamb", 7)
    customerC.validate_order(cashierA, stallB, "Lamb", 7)

    #case 4: the customer successfully places an order
    customerA.validate_order(cashierA, stallB, "Lamb", 8)
    customerB.validate_order(cashierA, stallB, "Lamb", 7)
    customerC.validate_order(cashierA, stallB, "Lamb", 7)
    #test add + commit

if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
