#!/usr/bin/env python3
"""
Lost & Found Data Detective - Process raw data and generate HTML dashboard
"""

import re
from collections import defaultdict
from difflib import SequenceMatcher
import json
from datetime import datetime

# Raw data as provided
raw_data = """
Day 1 Data: Opening Day Chaos (20 items)
blue scarf, found near ice rink, 2pm
BLUE SCARF - ice skating area - 2:15pm
Child's red mitten (left hand) hot cocoa stand
red mitten for kid, cocoa booth, around 2:30
iPhone 13 pro, black case, storytelling tent, 3pm
black iphone with case, story tent
KEYS - toyota key fob + house keys, parking lot
car keys (Toyota) and house keys - parking area - 3:45pm
wallet, brown leather, mens, fortune teller tent
Brown leather wallet (male), fortune tent, 4pm
purple beanie hat, ice rink
PURPLE HAT - knit beanie - ice skating
green scarf with snowflakes, storytelling area
Green scarf (snowflake pattern), story tent
black gloves (pair), parking lot
Black gloves (both), parking area, 5pm
AirPods case (white), ice rink
white airpods case, skating rink
pink phone case (no phone inside), fortune teller
Pink iPhone case (empty), fortune ten

Day 2 Data: Peak Crowd Day (35 items)
silver macbook pro, hot cocoa stand - URGENT
MacBook (silver) found at cocoa booth
Tesla key fob, parking lot - URGENT!!!
wedding ring, gold band, storytelling tent - VERY URGENT
Gold wedding ring, story tent - please help find owner!
grey backpack, small, kids, hot cocoa stand
child's gray backpack, cocoa booth
sunglasses (Ray-Ban), black, parking lot
Ray Ban sunglasses, black frames, parking
yellow scarf, ice rink
YELLOW SCARF - ice skating area
red scarf with white stripes, fortune teller
Red striped scarf, fortune tent
blue mittens (pair), ice rink
BLUE MITTENS - both hands - skating area
phone charger (iPhone lightning), storytelling tent
iphone charger cable, story tent
water bottle, blue metal, hot cocoa stand
Blue water bottle (stainless steel), cocoa booth
stuffed animal, brown teddy bear, ice rink - kid crying!
TEDDY BEAR brown, ice skating - child lost it
camera, Canon DSLR, black, parking lot - URGENT
Black Canon camera, parking area
white knit hat with pom pom, fortune teller
White pompom beanie, fortune tent
green gloves (pair), storytelling tent
Green gloves (both), story area
umbrella, black, parking lot
Black umbrella, parking
pink backpack, large, ice rink
PINK BACKPACK - big one - skating area
prescription glasses, black frames, hot cocoa stand
Black eyeglasses, cocoa booth
silver bracelet, ice rink
Silver bracelet (chain style), skating area
red wallet, womens, fortune teller
Red wallet (female), fortune tent
blue jacket, kids size, storytelling tent
Child's blue coat, story area

Day 3 Data: Family Frenzy Day (45 items)
laptop bag, black, empty, parking lot
Black laptop bag (no laptop inside), parking
white scarf, long, ice rink
WHITE SCARF - extra long - skating area
car keys - Honda key + 3 house keys, hot cocoa stand
Honda car key with house keys (3), cocoa booth
phone - Samsung Galaxy, cracked screen, storytelling tent - URGENT
Samsung phone (screen broken), story area - URGENT
brown boots, womens size 8, ice rink
Women's brown boots size 8, skating rink
red hat with ear flaps, fortune teller
RED HAT - ear flap style - fortune tent
black purse, small, crossbody style, parking lot
Small black crossbody purse, parking area
blue scarf, ice rink (again! different from yesterday)
BLUE SCARF - ice skating
green mittens, kids, hot cocoa stand
Child's green mittens, cocoa booth
wallet, black, mens, contains ID for "James Wilson", storytelling tent
Black male wallet - ID inside (James Wilson), story tent
yellow beanie, ice rink
Yellow knit hat, skating area
iPad, silver, in purple case, fortune teller - URGENT
Silver iPad with purple case, fortune tent - URGENT
grey scarf, long, parking lot
Gray scarf (long), parking
white gloves, pair, ice rink
White gloves (both), skating area
backpack, black, Northface brand, hot cocoa stand
Black North Face backpack, cocoa booth
sunglasses, aviator style, gold frames, parking lot
Gold aviator sunglasses, parking
red scarf, storytelling tent
RED SCARF, story area
phone case, clear with sparkles, no phone, ice rink
Clear sparkly phone case (empty), skating rink
brown wallet, womens, fortune teller
Brown female wallet, fortune tent
blue jacket, adult size large, parking lot
Blue jacket (L), parking area
keys - apartment keys on Eiffel Tower keychain, hot cocoa stand
Apartment keys (Eiffel Tower keyring), cocoa booth
black beanie, ice rink
BLACK BEANIE, skating area
pink scarf, storytelling tent
Pink scarf, story area
watch, silver Fitbit, ice rink - URGENT
Silver Fitbit watch, skating area - URGENT
green jacket, kids, hot cocoa stand
Child's green coat, cocoa booth
white mittens, pair, fortune teller
White mittens (both), fortune tent
umbrella, red, parking lot
Red umbrella, parking
brown gloves, leather, mens, ice rink
Men's brown leather gloves, skating area
phone charger, USB-C, storytelling tent
USB-C charging cable, story area
water bottle, pink, hot cocoa stand
Pink water bottle, cocoa booth
grey hat, beanie style, parking lot
Gray beanie, parking
blue backpack, small, kids, ice rink
Small child's blue backpack, skating rink
black scarf, fortune teller
BLACK SCARF, fortune tent
yellow gloves, pair, storytelling tent
Yellow gloves (both), story area
sunglasses, black, hot cocoa stand
Black sunglasses, cocoa booth
red mittens, kids, ice rink
Child's red mittens, skating area
white scarf, short, parking lot
White scarf (short), parking
green hat, fortune teller
Green hat, fortune tent
"""

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def parse_raw_data(raw_text):
    """Parse raw data into structured format"""
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    items = []
    current_day = None
    
    for line in lines:
        # Skip day headers
        if line.startswith('Day'):
            current_day = line
            continue
        
        # Skip empty lines
        if not line:
            continue
            
        # Extract basic info from each line
        item = {
            'raw_text': line,
            'day': current_day,
            'urgent': 'URGENT' in line.upper() or 'crying' in line.lower() or 'help find owner' in line.lower()
        }
        
        # Parse item description
        item_text = re.sub(r'\s*-\s*URGENT[!]*\s*', '', line, flags=re.IGNORECASE)
        item_text = re.sub(r'\s*-\s*VERY URGENT\s*', '', item_text, flags=re.IGNORECASE)
        item_text = re.sub(r'\s*-\s*kid crying[!]*\s*', '', item_text, flags=re.IGNORECASE)
        item_text = re.sub(r'\s*-\s*please help find owner[!]*\s*', '', item_text, flags=re.IGNORECASE)
        item_text = re.sub(r'\s*-\s*child lost it\s*', '', item_text, flags=re.IGNORECASE)
        
        # Standardize locations
        location_mapping = {
            'ice rink': 'Ice Rink',
            'ice skating area': 'Ice Rink',
            'ice skating': 'Ice Rink',
            'skating rink': 'Ice Rink',
            'skating area': 'Ice Rink',
            'hot cocoa stand': 'Hot Cocoa Stand',
            'cocoa booth': 'Hot Cocoa Stand',
            'cocoa stand': 'Hot Cocoa Stand',
            'storytelling tent': 'Storytelling Tent',
            'storytelling area': 'Storytelling Tent',
            'story tent': 'Storytelling Tent',
            'story area': 'Storytelling Tent',
            'fortune teller tent': 'Fortune Teller Tent',
            'fortune teller': 'Fortune Teller Tent',
            'fortune tent': 'Fortune Teller Tent',
            'parking lot': 'Parking Lot',
            'parking area': 'Parking Lot',
            'parking': 'Parking Lot'
        }
        
        location = 'Unknown'
        for loc_key, loc_value in location_mapping.items():
            if loc_key in item_text.lower():
                location = loc_value
                break
        
        item['location'] = location
        
        # Clean up item description (remove location and time info)
        description = item_text
        for loc_key in location_mapping.keys():
            description = re.sub(rf'\b{re.escape(loc_key)}\b', '', description, flags=re.IGNORECASE)
        
        # Remove time references
        description = re.sub(r'\b\d{1,2}(:\d{2})?\s*pm\b', '', description, flags=re.IGNORECASE)
        description = re.sub(r'\b\d{1,2}(:\d{2})?\s*am\b', '', description, flags=re.IGNORECASE)
        description = re.sub(r'\baround\s+', '', description, flags=re.IGNORECASE)
        description = re.sub(r'\bfound\s+(near|at|in)\s*', '', description, flags=re.IGNORECASE)
        description = re.sub(r'\bfound\s*', '', description, flags=re.IGNORECASE)
        
        # Clean up punctuation and whitespace
        description = re.sub(r'[,-]+\s*$', '', description)
        description = re.sub(r'^[,-]+\s*', '', description)
        description = re.sub(r'\s*-+\s*', ' ', description)
        description = re.sub(r'\s+', ' ', description)
        description = description.strip(' ,-')
        
        item['description'] = description
        
        items.append(item)
    
    return items

def deduplicate_items(items):
    """Remove duplicates using fuzzy matching"""
    unique_items = []
    
    for item in items:
        is_duplicate = False
        
        for unique_item in unique_items:
            # Check similarity of descriptions
            desc_similarity = similarity(item['description'], unique_item['description'])
            
            # Check if same location
            same_location = item['location'] == unique_item['location']
            
            # Consider it a duplicate if high similarity and same location
            if desc_similarity > 0.8 and same_location:
                is_duplicate = True
                # Keep the more detailed description or urgent flag
                if item['urgent'] and not unique_item['urgent']:
                    unique_item['urgent'] = True
                if len(item['description']) > len(unique_item['description']):
                    unique_item['description'] = item['description']
                break
        
        if not is_duplicate:
            unique_items.append(item)
    
    return unique_items

def categorize_item(description):
    """Categorize items based on description"""
    description_lower = description.lower()
    
    electronics_keywords = ['iphone', 'phone', 'ipad', 'macbook', 'laptop', 'camera', 'airpods', 'charger', 'fitbit', 'watch']
    clothing_keywords = ['scarf', 'gloves', 'mittens', 'hat', 'beanie', 'jacket', 'coat', 'boots']
    personal_keywords = ['wallet', 'purse', 'keys', 'ring', 'bracelet', 'glasses', 'sunglasses']
    accessories_keywords = ['backpack', 'umbrella', 'water bottle', 'phone case', 'laptop bag']
    
    for keyword in electronics_keywords:
        if keyword in description_lower:
            return 'Electronics'
    
    for keyword in clothing_keywords:
        if keyword in description_lower:
            return 'Clothing'
    
    for keyword in personal_keywords:
        if keyword in description_lower:
            return 'Personal Items'
    
    for keyword in accessories_keywords:
        if keyword in description_lower:
            return 'Accessories'
    
    return 'Other'

def flag_urgent_items(items):
    """Flag urgent items based on category and content"""
    for item in items:
        category = categorize_item(item['description'])
        description_lower = item['description'].lower()
        
        # Electronics are generally urgent
        if category == 'Electronics':
            item['urgent'] = True
        
        # Keys and wallets are urgent
        if 'keys' in description_lower or 'key' in description_lower:
            item['urgent'] = True
        
        if 'wallet' in description_lower or 'purse' in description_lower:
            item['urgent'] = True
        
        # Items with ID information
        if 'id' in description_lower:
            item['urgent'] = True
        
        # Wedding rings
        if 'wedding ring' in description_lower:
            item['urgent'] = True
    
    return items

def generate_html_dashboard(items):
    """Generate complete HTML dashboard"""
    
    # Calculate statistics
    total_items = len(items)
    urgent_items = sum(1 for item in items if item['urgent'])
    
    # Count by category
    categories = defaultdict(int)
    for item in items:
        category = categorize_item(item['description'])
        categories[category] += 1
    
    # Count by location
    locations = defaultdict(int)
    for item in items:
        locations[item['location']] += 1
    
    # Sort items - urgent first, then by category
    sorted_items = sorted(items, key=lambda x: (not x['urgent'], categorize_item(x['description']), x['description']))
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Winter Festival Lost & Found Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #ffebee 100%);
            color: #1a237e;
            line-height: 1.6;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(45deg, #1565c0, #c62828);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}

        .header p {{
            font-size: 1.2em;
            color: #424242;
            margin-bottom: 5px;
        }}

        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 2px solid #e3f2fd;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}

        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #1565c0;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 1em;
            color: #666;
            font-weight: 500;
        }}

        .urgent-section {{
            background: linear-gradient(135deg, #ffcdd2, #ffebee);
            border: 2px solid #d32f2f;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(211, 47, 47, 0.2);
        }}

        .urgent-title {{
            color: #c62828;
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .urgent-title::before {{
            content: "🚨";
            font-size: 1.2em;
        }}

        .controls {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border: 2px solid #e3f2fd;
        }}

        .search-box {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #e3f2fd;
            border-radius: 25px;
            font-size: 1em;
            margin-bottom: 15px;
            transition: border-color 0.3s ease;
        }}

        .search-box:focus {{
            outline: none;
            border-color: #1565c0;
            box-shadow: 0 0 10px rgba(21, 101, 192, 0.3);
        }}

        .filters {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .filter-group {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .filter-label {{
            font-weight: 500;
            color: #1a237e;
        }}

        .filter-select {{
            padding: 8px 15px;
            border: 2px solid #e3f2fd;
            border-radius: 20px;
            background: white;
            font-size: 0.9em;
            transition: border-color 0.3s ease;
        }}

        .filter-select:focus {{
            outline: none;
            border-color: #1565c0;
        }}

        .table-container {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 2px solid #e3f2fd;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th {{
            background: linear-gradient(135deg, #1565c0, #1976d2);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
            transition: background 0.3s ease;
        }}

        th:hover {{
            background: linear-gradient(135deg, #0d47a1, #1565c0);
        }}

        th::after {{
            content: ' ⇅';
            font-size: 0.8em;
            opacity: 0.7;
        }}

        td {{
            padding: 15px;
            border-bottom: 1px solid #e3f2fd;
        }}

        tr:nth-child(even) {{
            background-color: #fafafa;
        }}

        tr:hover {{
            background-color: #e8f4fd;
        }}

        .urgent-row {{
            background: linear-gradient(135deg, #ffebee, #ffcdd2) !important;
            border-left: 4px solid #d32f2f;
        }}

        .urgent-row:hover {{
            background: linear-gradient(135deg, #ffcdd2, #ffbdd2) !important;
        }}

        .category {{
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 500;
            display: inline-block;
        }}

        .category-electronics {{
            background: #e8f5e8;
            color: #2e7d32;
            border: 1px solid #4caf50;
        }}

        .category-clothing {{
            background: #fff3e0;
            color: #ef6c00;
            border: 1px solid #ff9800;
        }}

        .category-personal {{
            background: #fce4ec;
            color: #c2185b;
            border: 1px solid #e91e63;
        }}

        .category-accessories {{
            background: #e1f5fe;
            color: #0277bd;
            border: 1px solid #03a9f4;
        }}

        .category-other {{
            background: #f3e5f5;
            color: #7b1fa2;
            border: 1px solid #9c27b0;
        }}

        .urgent-badge {{
            background: #d32f2f;
            color: white;
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 0.75em;
            font-weight: bold;
            margin-left: 8px;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
            100% {{ opacity: 1; }}
        }}

        .no-results {{
            text-align: center;
            padding: 40px;
            color: #666;
            font-style: italic;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}

            .header h1 {{
                font-size: 2em;
            }}

            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .filters {{
                flex-direction: column;
                align-items: stretch;
            }}

            .filter-group {{
                flex-direction: column;
            }}

            .table-container {{
                overflow-x: auto;
            }}

            table {{
                min-width: 600px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>❄️ Winter Festival Lost & Found Dashboard ❄️</h1>
            <p>Your trusted companion for reuniting lost treasures with their owners</p>
            <div class="timestamp">Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_items}</div>
                <div class="stat-label">Total Items</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{urgent_items}</div>
                <div class="stat-label">Urgent Items</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(categories)}</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(locations)}</div>
                <div class="stat-label">Locations</div>
            </div>
        </div>"""

    # Add urgent section if there are urgent items
    if urgent_items > 0:
        urgent_list = [item for item in sorted_items if item['urgent']]
        html += f"""
        <div class="urgent-section">
            <div class="urgent-title">Urgent Items Requiring Immediate Attention</div>
            <table>
                <thead>
                    <tr>
                        <th>Item Description</th>
                        <th>Category</th>
                        <th>Location</th>
                    </tr>
                </thead>
                <tbody>"""
        
        for item in urgent_list[:10]:  # Show top 10 urgent items
            category = categorize_item(item['description'])
            category_class = category.lower().replace(' ', '-')
            html += f"""
                    <tr class="urgent-row">
                        <td>{item['description']} <span class="urgent-badge">URGENT</span></td>
                        <td><span class="category category-{category_class}">{category}</span></td>
                        <td>{item['location']}</td>
                    </tr>"""
        
        if len(urgent_list) > 10:
            html += f"""
                    <tr>
                        <td colspan="3" style="text-align: center; font-style: italic; color: #666;">
                            ... and {len(urgent_list) - 10} more urgent items in the full inventory below
                        </td>
                    </tr>"""
        
        html += """
                </tbody>
            </table>
        </div>"""

    # Continue with main inventory
    html += """
        <div class="controls">
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search for items by description, category, or location...">
            <div class="filters">
                <div class="filter-group">
                    <label class="filter-label">Category:</label>
                    <select class="filter-select" id="categoryFilter">
                        <option value="">All Categories</option>"""
    
    for category in sorted(categories.keys()):
        html += f'<option value="{category}">{category}</option>'
    
    html += """
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Location:</label>
                    <select class="filter-select" id="locationFilter">
                        <option value="">All Locations</option>"""
    
    for location in sorted(locations.keys()):
        html += f'<option value="{location}">{location}</option>'
    
    html += """
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Urgency:</label>
                    <select class="filter-select" id="urgencyFilter">
                        <option value="">All Items</option>
                        <option value="urgent">Urgent Only</option>
                        <option value="normal">Normal Only</option>
                    </select>
                </div>
            </div>
        </div>

        <div class="table-container">
            <table id="inventoryTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Item Description</th>
                        <th onclick="sortTable(1)">Category</th>
                        <th onclick="sortTable(2)">Location</th>
                        <th onclick="sortTable(3)">Status</th>
                    </tr>
                </thead>
                <tbody id="tableBody">"""
    
    for i, item in enumerate(sorted_items):
        category = categorize_item(item['description'])
        category_class = category.lower().replace(' ', '-')
        row_class = 'urgent-row' if item['urgent'] else ''
        urgent_badge = '<span class="urgent-badge">URGENT</span>' if item['urgent'] else ''
        
        html += f"""
                    <tr class="{row_class}" data-category="{category}" data-location="{item['location']}" data-urgent="{'urgent' if item['urgent'] else 'normal'}">
                        <td>{item['description']}{urgent_badge}</td>
                        <td><span class="category category-{category_class}">{category}</span></td>
                        <td>{item['location']}</td>
                        <td>{'🚨 Needs Immediate Attention' if item['urgent'] else '📋 Available for Pickup'}</td>
                    </tr>"""
    
    html += """
                </tbody>
            </table>
            <div class="no-results" id="noResults" style="display: none;">
                No items match your search criteria. Try adjusting your filters or search terms.
            </div>
        </div>
    </div>

    <script>
        let currentSort = {column: -1, ascending: true};

        function sortTable(columnIndex) {
            const table = document.getElementById('inventoryTable');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr')).filter(row => row.style.display !== 'none');
            
            // Toggle sort direction
            if (currentSort.column === columnIndex) {
                currentSort.ascending = !currentSort.ascending;
            } else {
                currentSort.ascending = true;
            }
            currentSort.column = columnIndex;

            rows.sort((a, b) => {
                const aText = a.cells[columnIndex].textContent.toLowerCase();
                const bText = b.cells[columnIndex].textContent.toLowerCase();
                
                if (aText < bText) return currentSort.ascending ? -1 : 1;
                if (aText > bText) return currentSort.ascending ? 1 : -1;
                return 0;
            });

            // Re-append sorted rows
            rows.forEach(row => tbody.appendChild(row));
            
            // Update header indicators
            const headers = table.querySelectorAll('th');
            headers.forEach((header, index) => {
                if (index === columnIndex) {
                    header.style.background = 'linear-gradient(135deg, #0d47a1, #1565c0)';
                    header.innerHTML = header.innerHTML.replace(/[⇅↑↓]/, currentSort.ascending ? '↑' : '↓');
                } else {
                    header.style.background = 'linear-gradient(135deg, #1565c0, #1976d2)';
                    header.innerHTML = header.innerHTML.replace(/[⇅↑↓]/, '⇅');
                }
            });
        }

        function filterTable() {
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            const categoryFilter = document.getElementById('categoryFilter').value;
            const locationFilter = document.getElementById('locationFilter').value;
            const urgencyFilter = document.getElementById('urgencyFilter').value;
            
            const rows = document.querySelectorAll('#tableBody tr');
            let visibleCount = 0;
            
            rows.forEach(row => {
                const description = row.cells[0].textContent.toLowerCase();
                const category = row.dataset.category;
                const location = row.dataset.location;
                const urgency = row.dataset.urgent;
                
                const matchesSearch = description.includes(searchTerm) || 
                                    category.toLowerCase().includes(searchTerm) || 
                                    location.toLowerCase().includes(searchTerm);
                const matchesCategory = !categoryFilter || category === categoryFilter;
                const matchesLocation = !locationFilter || location === locationFilter;
                const matchesUrgency = !urgencyFilter || urgency === urgencyFilter;
                
                if (matchesSearch && matchesCategory && matchesLocation && matchesUrgency) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            // Show/hide no results message
            const noResults = document.getElementById('noResults');
            const tableBody = document.getElementById('tableBody');
            if (visibleCount === 0) {
                noResults.style.display = 'block';
                tableBody.style.display = 'none';
            } else {
                noResults.style.display = 'none';
                tableBody.style.display = '';
            }
        }

        // Add event listeners
        document.getElementById('searchBox').addEventListener('input', filterTable);
        document.getElementById('categoryFilter').addEventListener('change', filterTable);
        document.getElementById('locationFilter').addEventListener('change', filterTable);
        document.getElementById('urgencyFilter').addEventListener('change', filterTable);

        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            // Sort by urgency initially (urgent items first)
            sortTable(3);
        });
    </script>
</body>
</html>"""
    
    return html

# Main processing
def main():
    print("🔍 Lost & Found Data Detective Processing...")
    
    # Step 1: Parse raw data
    print("📊 Parsing raw data...")
    items = parse_raw_data(raw_data)
    print(f"   Found {len(items)} raw items")
    
    # Step 2: Deduplicate
    print("🔄 Deduplicating items...")
    unique_items = deduplicate_items(items)
    print(f"   Deduplicated to {len(unique_items)} unique items")
    
    # Step 3: Categorize and flag urgent
    print("🏷️  Categorizing items...")
    for item in unique_items:
        item['category'] = categorize_item(item['description'])
    
    print("🚨 Flagging urgent items...")
    flagged_items = flag_urgent_items(unique_items)
    urgent_count = sum(1 for item in flagged_items if item['urgent'])
    print(f"   Found {urgent_count} urgent items")
    
    # Step 4: Generate HTML dashboard
    print("🎨 Generating HTML dashboard...")
    html_content = generate_html_dashboard(flagged_items)
    
    # Save to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Dashboard generated successfully!")
    print(f"📁 Saved as: index.html")
    print(f"📈 Total items: {len(flagged_items)}")
    print(f"🚨 Urgent items: {urgent_count}")
    
    return html_content

if __name__ == "__main__":
    main()
