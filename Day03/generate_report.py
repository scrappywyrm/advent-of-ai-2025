import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import matplotlib.patches as mpatches

# Winter Festival Palette
COLORS = {
    'primary': '#0b1026',    # Dark navy
    'accent': '#ffd700',     # Gold
    'light': '#e6e6fa',      # Lavender
    'highlight': '#d62728'   # Red
}

# Set up the figure style
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.color'] = 'lightgray'
plt.rcParams['grid.alpha'] = 0.7

def create_bar_chart():
    """Chart 1: Final Championship Results - Vertical Bar Chart"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Final match data
    contestants = ['Dark Chocolate\nDecadence', 'Peppermint\nDream']
    votes = [678, 623]
    colors = [COLORS['accent'], COLORS['light']]
    
    bars = ax.bar(contestants, votes, color=colors, edgecolor=COLORS['primary'], linewidth=2)
    
    # Add value labels on bars
    for bar, vote in zip(bars, votes):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{vote} votes', ha='center', va='bottom', 
                fontweight='bold', color=COLORS['primary'])
    
    # Styling
    ax.set_title('Final Championship Results', fontsize=16, fontweight='bold', 
                 color=COLORS['primary'], pad=20)
    ax.set_ylabel('Votes', fontsize=12, fontweight='bold', color=COLORS['primary'])
    ax.set_ylim(0, max(votes) * 1.1)
    
    # Grid styling
    ax.grid(True, axis='y', linestyle='-', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['primary'])
    ax.spines['bottom'].set_color(COLORS['primary'])
    
    # Add winner annotation
    ax.annotate('🏆 WINNER!', xy=(0, 678), xytext=(0, 720),
                ha='center', fontsize=14, fontweight='bold',
                color=COLORS['highlight'],
                arrowprops=dict(arrowstyle='->', color=COLORS['highlight']))
    
    plt.tight_layout()
    plt.savefig('bar_results.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()

def create_pie_chart():
    """Chart 2: Voting Period Distribution - Pie Chart"""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Voting period data
    periods = ['Morning', 'Afternoon', 'Evening']
    votes = [1247, 1891, 2156]
    colors = [COLORS['light'], COLORS['accent'], COLORS['primary']]
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(votes, labels=periods, colors=colors, 
                                      autopct='%1.1f%%', startangle=90,
                                      textprops={'fontsize': 11, 'fontweight': 'bold'})
    
    # Style the percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # Style the labels
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')
        text.set_color(COLORS['primary'])
    
    ax.set_title('Voting Period Distribution', fontsize=16, fontweight='bold',
                 color=COLORS['primary'], pad=20)
    
    # Add vote counts in legend
    legend_labels = [f'{period}: {vote:,} votes' for period, vote in zip(periods, votes)]
    ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    plt.savefig('pie_votes.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

def create_radar_chart():
    """Chart 3: Recipe Attributes Comparison - Radar Chart"""
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Recipe data (top 4 finalists)
    recipes = {
        'Dark Chocolate Decadence': [10, 5, 8, 10],  # Winner
        'Peppermint Dream': [6, 9, 7, 9],           # Runner-up
        'Classic Swiss Velvet': [8, 6, 4, 7],      # Semifinalist
        'Cinnamon Fireside': [7, 7, 8, 8]          # Semifinalist
    }
    
    attributes = ['Richness', 'Sweetness', 'Creativity', 'Presentation']
    
    # Number of variables
    N = len(attributes)
    
    # Angle for each attribute
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete the circle
    
    # Colors for each recipe
    recipe_colors = [COLORS['accent'], COLORS['light'], COLORS['primary'], COLORS['highlight']]
    
    # Plot each recipe
    for i, (recipe, scores) in enumerate(recipes.items()):
        scores += scores[:1]  # Complete the circle
        ax.plot(angles, scores, 'o-', linewidth=2, label=recipe, 
                color=recipe_colors[i], markersize=6)
        ax.fill(angles, scores, alpha=0.25, color=recipe_colors[i])
    
    # Add attribute labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes, fontsize=11, fontweight='bold', 
                       color=COLORS['primary'])
    
    # Set y-axis
    ax.set_ylim(0, 10)
    ax.set_yticks(range(0, 11, 2))
    ax.set_yticklabels([str(i) for i in range(0, 11, 2)], 
                       fontsize=9, color=COLORS['primary'])
    
    # Grid styling
    ax.grid(True, color='lightgray', alpha=0.5)
    
    # Title
    ax.set_title('Recipe Attributes Comparison\n(Top 4 Finalists)', 
                 fontsize=16, fontweight='bold', color=COLORS['primary'], 
                 pad=30)
    
    # Legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
    
    plt.tight_layout()
    plt.savefig('radar_comparison.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

def print_summary():
    """Print tournament summary statistics"""
    print("🍫 HOT COCOA TOURNAMENT VISUALIZATION COMPLETE! 🍫")
    print("=" * 50)
    print("Charts Generated:")
    print("📊 bar_results.png - Final Championship Results")
    print("🥧 pie_votes.png - Voting Period Distribution") 
    print("🕸️ radar_comparison.png - Recipe Attributes Comparison")
    print()
    print("Tournament Highlights:")
    print("🏆 Winner: Dark Chocolate Decadence (678 votes)")
    print("🥈 Runner-up: Peppermint Dream (623 votes)")
    print("📊 Total Votes Cast: 5,294")
    print("🔥 Closest Match: Peppermint Dream vs Salted Caramel Swirl (14 vote margin)")
    print("💥 Biggest Blowout: Dark Chocolate Decadence vs White Chocolate Wonder (73 vote margin)")

if __name__ == "__main__":
    print("Generating Hot Cocoa Tournament Visualizations...")
    
    create_bar_chart()
    print("✅ Bar chart created: bar_results.png")
    
    create_pie_chart()
    print("✅ Pie chart created: pie_votes.png")
    
    create_radar_chart()
    print("✅ Radar chart created: radar_comparison.png")
    
    print_summary()