import requests
import time

# Configuration
BASE_URL = "http://baris.org"
EDIT_URL = f"{BASE_URL}/edit/"

# Your cookies (update these with your actual values)
COOKIES = {
    'csrftoken': 'SoETQqt5Zp7RJaokCmKXPYp9vokmm5an',
    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1NDUyMTk2LCJpYXQiOjE3NjU0NDg1OTYsInN1YiI6ImFkbWluIn0.mplycMYe2wK4gMMCngU0llQPqLHZAz73qiE8s6B0J7Y'
}

# All menu items from your HTML
MENU_ITEMS = [
    # LATTES
    {'item_name': 'Classic Espresso', 'item_price': '3.50', 'item_icon': '☕', 'item_category': 'lattes', 'item_description': 'Rich, bold shot of our finest espresso beans'},
    {'item_name': 'Cappuccino', 'item_price': '4.50', 'item_icon': '🥛', 'item_category': 'lattes', 'item_description': 'Espresso with steamed milk and thick foam'},
    {'item_name': 'Caffe Latte', 'item_price': '4.75', 'item_icon': '☕', 'item_category': 'lattes', 'item_description': 'Smooth espresso with velvety steamed milk'},
    {'item_name': 'Vanilla Latte', 'item_price': '5.25', 'item_icon': '🍯', 'item_category': 'lattes', 'item_description': 'Our latte enhanced with sweet vanilla syrup'},
    {'item_name': 'Caramel Macchiato', 'item_price': '5.50', 'item_icon': '🍫', 'item_category': 'lattes', 'item_description': 'Espresso marked with vanilla and caramel drizzle'},
    {'item_name': 'Hazelnut Latte', 'item_price': '5.25', 'item_icon': '🌰', 'item_category': 'lattes', 'item_description': 'Nutty sweetness combined with smooth espresso'},
    
    # ON ICE
    {'item_name': 'Iced Americano', 'item_price': '4.00', 'item_icon': '🧊', 'item_category': 'ice', 'item_description': 'Espresso shots over ice with cold water'},
    {'item_name': 'Iced Latte', 'item_price': '4.75', 'item_icon': '🧊', 'item_category': 'ice', 'item_description': 'Chilled espresso with cold milk over ice'},
    {'item_name': 'Iced Caramel Latte', 'item_price': '5.25', 'item_icon': '🧊', 'item_category': 'ice', 'item_description': 'Sweet caramel meets iced espresso perfection'},
    {'item_name': 'Iced Mocha', 'item_price': '5.50', 'item_icon': '🧊', 'item_category': 'ice', 'item_description': 'Chocolate and espresso over ice with cold milk'},
    {'item_name': 'Cold Brew', 'item_price': '4.50', 'item_icon': '🧊', 'item_category': 'ice', 'item_description': 'Smooth, slow-steeped coffee served over ice'},
    {'item_name': 'Vanilla Cold Brew', 'item_price': '5.00', 'item_icon': '🧊', 'item_category': 'ice', 'item_description': 'Our signature cold brew with vanilla cream'},
    
    # BLENDED
    {'item_name': 'Mocha Frappé', 'item_price': '6.00', 'item_icon': '🌪️', 'item_category': 'blended', 'item_description': 'Blended coffee with chocolate and ice'},
    {'item_name': 'Caramel Frappé', 'item_price': '6.00', 'item_icon': '🌪️', 'item_category': 'blended', 'item_description': 'Sweet caramel blended with coffee and ice'},
    {'item_name': 'Vanilla Bean Frappé', 'item_price': '5.75', 'item_icon': '🌪️', 'item_category': 'blended', 'item_description': 'Creamy vanilla blended drink with ice'},
    {'item_name': 'Java Chip Frappé', 'item_price': '6.25', 'item_icon': '🌪️', 'item_category': 'blended', 'item_description': 'Coffee blended with chocolate chips and ice'},
    {'item_name': 'White Chocolate Frappé', 'item_price': '6.25', 'item_icon': '🌪️', 'item_category': 'blended', 'item_description': 'Smooth white chocolate blended coffee'},
    {'item_name': 'Espresso Frappé', 'item_price': '5.75', 'item_icon': '🌪️', 'item_category': 'blended', 'item_description': 'Bold espresso blended with ice and cream'},
    
    # BREWED COFFEES & TEAS
    {'item_name': 'Pike Place Roast', 'item_price': '3.00', 'item_icon': '☕', 'item_category': 'brewed', 'item_description': 'Our signature medium roast coffee'},
    {'item_name': 'Dark Roast', 'item_price': '3.00', 'item_icon': '☕', 'item_category': 'brewed', 'item_description': 'Bold and full-bodied dark roast'},
    {'item_name': 'Decaf Coffee', 'item_price': '3.00', 'item_icon': '☕', 'item_category': 'brewed', 'item_description': 'Rich flavor without the caffeine'},
    {'item_name': 'Earl Grey Tea', 'item_price': '3.25', 'item_icon': '🍵', 'item_category': 'brewed', 'item_description': 'Classic black tea with bergamot'},
    {'item_name': 'Green Tea', 'item_price': '3.25', 'item_icon': '🍵', 'item_category': 'brewed', 'item_description': 'Fresh and revitalizing green tea'},
    {'item_name': 'Chamomile Tea', 'item_price': '3.25', 'item_icon': '🍵', 'item_category': 'brewed', 'item_description': 'Soothing herbal tea blend'},
    
    # TEA LATTES
    {'item_name': 'Chai Tea Latte', 'item_price': '4.75', 'item_icon': '🍵', 'item_category': 'tea-lattes', 'item_description': 'Spiced black tea with steamed milk'},
    {'item_name': 'Matcha Latte', 'item_price': '5.25', 'item_icon': '🍵', 'item_category': 'tea-lattes', 'item_description': 'Premium Japanese green tea with steamed milk'},
    {'item_name': 'London Fog', 'item_price': '4.75', 'item_icon': '🍵', 'item_category': 'tea-lattes', 'item_description': 'Earl Grey tea with vanilla and steamed milk'},
    {'item_name': 'Turmeric Latte', 'item_price': '5.00', 'item_icon': '🍵', 'item_category': 'tea-lattes', 'item_description': 'Golden milk with turmeric and warm spices'},
    {'item_name': 'Rooibos Latte', 'item_price': '4.75', 'item_icon': '🍵', 'item_category': 'tea-lattes', 'item_description': 'Caffeine-free red tea with steamed milk'},
    {'item_name': 'Honey Lavender Latte', 'item_price': '5.25', 'item_icon': '🍵', 'item_category': 'tea-lattes', 'item_description': 'Floral lavender with honey and steamed milk'},
    
    # HOT CHOCOLATES
    {'item_name': 'Classic Hot Chocolate', 'item_price': '4.50', 'item_icon': '🍫', 'item_category': 'chocolates', 'item_description': 'Rich chocolate with steamed milk and whipped cream'},
    {'item_name': 'Dark Hot Chocolate', 'item_price': '4.75', 'item_icon': '🍫', 'item_category': 'chocolates', 'item_description': 'Intense dark chocolate for the chocolate lover'},
    {'item_name': 'White Hot Chocolate', 'item_price': '4.75', 'item_icon': '🍫', 'item_category': 'chocolates', 'item_description': 'Smooth and creamy white chocolate delight'},
    {'item_name': 'Mint Hot Chocolate', 'item_price': '5.00', 'item_icon': '🍫', 'item_category': 'chocolates', 'item_description': 'Refreshing mint infused hot chocolate'},
    {'item_name': 'Salted Caramel Hot Chocolate', 'item_price': '5.25', 'item_icon': '🍫', 'item_category': 'chocolates', 'item_description': 'Sweet and salty chocolate perfection'},
    {'item_name': 'Mexican Spiced Hot Chocolate', 'item_price': '5.25', 'item_icon': '🍫', 'item_category': 'chocolates', 'item_description': 'Hot chocolate with cinnamon and a hint of chili'},
    
    # SMOOTHIES
    {'item_name': 'Berry Blast', 'item_price': '6.50', 'item_icon': '🍓', 'item_category': 'smoothies', 'item_description': 'Strawberries, blueberries, raspberries, and banana'},
    {'item_name': 'Tropical Paradise', 'item_price': '6.50', 'item_icon': '🥭', 'item_category': 'smoothies', 'item_description': 'Mango, pineapple, coconut, and orange juice'},
    {'item_name': 'Peanut Butter Banana', 'item_price': '6.75', 'item_icon': '🍌', 'item_category': 'smoothies', 'item_description': 'Banana, peanut butter, honey, and almond milk'},
    {'item_name': 'Green Machine', 'item_price': '7.00', 'item_icon': '🥬', 'item_category': 'smoothies', 'item_description': 'Spinach, kale, banana, mango, and apple juice'},
    {'item_name': 'Peach Perfection', 'item_price': '6.50', 'item_icon': '🍑', 'item_category': 'smoothies', 'item_description': 'Peaches, strawberries, yogurt, and orange juice'},
    {'item_name': 'Acai Power Bowl', 'item_price': '8.00', 'item_icon': '🫐', 'item_category': 'smoothies', 'item_description': 'Acai, mixed berries, granola, and honey (drinkable)'},
    
    # FOOD
    {'item_name': 'Butter Croissant', 'item_price': '3.50', 'item_icon': '🥐', 'item_category': 'food', 'item_description': 'Flaky, buttery French pastry'},
    {'item_name': 'Everything Bagel', 'item_price': '4.00', 'item_icon': '🥯', 'item_category': 'food', 'item_description': 'Toasted bagel with cream cheese'},
    {'item_name': 'Turkey Avocado Sandwich', 'item_price': '8.50', 'item_icon': '🥪', 'item_category': 'food', 'item_description': 'Turkey, avocado, lettuce, tomato on artisan bread'},
    {'item_name': 'Caprese Panini', 'item_price': '8.00', 'item_icon': '🥪', 'item_category': 'food', 'item_description': 'Fresh mozzarella, tomato, basil, balsamic glaze'},
    {'item_name': 'Caesar Salad', 'item_price': '7.50', 'item_icon': '🥗', 'item_category': 'food', 'item_description': 'Romaine, parmesan, croutons, Caesar dressing'},
    {'item_name': 'Blueberry Muffin', 'item_price': '3.75', 'item_icon': '🧁', 'item_category': 'food', 'item_description': 'Freshly baked with plump blueberries'},
    {'item_name': 'Chocolate Chip Cookie', 'item_price': '2.50', 'item_icon': '🍪', 'item_category': 'food', 'item_description': 'Warm, gooey chocolate chip cookie'},
    {'item_name': 'Apple Pie Slice', 'item_price': '4.50', 'item_icon': '🥧', 'item_category': 'food', 'item_description': 'Classic apple pie with cinnamon'},
    {'item_name': 'Carrot Cake', 'item_price': '5.00', 'item_icon': '🍰', 'item_category': 'food', 'item_description': 'Moist carrot cake with cream cheese frosting'},
    {'item_name': 'Avocado Toast', 'item_price': '7.00', 'item_icon': '🥖', 'item_category': 'food', 'item_description': 'Smashed avocado on sourdough with cherry tomatoes'},
]

def add_menu_item(item_data, csrf_token):
    """Send POST request to add a menu item"""
    
    headers = {
        'X-CSRFToken': csrf_token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': EDIT_URL,
    }
    
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'item_id': '',  # Empty for new items
        'item_name': item_data['item_name'],
        'item_price': item_data['item_price'],
        'item_icon': item_data['item_icon'],
        'item_category': item_data['item_category'],
        'item_description': item_data['item_description']
    }
    
    try:
        response = requests.post(
            EDIT_URL,
            headers=headers,
            cookies=COOKIES,
            data=data
        )
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Add all menu items to the database"""
    
    print("🍵 Bean Haven - Menu Items Uploader")
    print("=" * 60)
    
    csrf_token = COOKIES['csrftoken']
    
    total = len(MENU_ITEMS)
    success_count = 0
    failed_count = 0
    
    for idx, item in enumerate(MENU_ITEMS, 1):
        print(f"\n[{idx}/{total}] Adding: {item['item_name']}")
        print(f"  Category: {item['item_category']} | Price: ${item['item_price']}")
        
        response = add_menu_item(item, csrf_token)
        
        if response and response.status_code == 200:
            print(f"  ✓ Success!")
            success_count += 1
        else:
            print(f"  ✗ Failed - Status: {response.status_code if response else 'No response'}")
            failed_count += 1
        
        # Small delay between requests
        time.sleep(0.3)
    
    print("\n" + "=" * 60)
    print(f"📊 Summary:")
    print(f"   Total items: {total}")
    print(f"   ✓ Success: {success_count}")
    print(f"   ✗ Failed: {failed_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()