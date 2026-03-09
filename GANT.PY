import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

# Set up the figure
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor('white')

# Define phases only
phases = [
    ('Phase 1: Planning', 1, 7, '#3498db'),
    ('Phase 2: Database', 8, 7, '#9b59b6'),
    ('Phase 3: Backend Core', 15, 9, '#e74c3c'),
    ('Phase 4: Backend Advanced', 24, 10, '#c0392b'),
    ('Phase 5: Frontend', 34, 9, '#2ecc71'),
    ('Phase 6: Testing', 43, 7, '#f39c12'),
    ('Phase 7: Documentation', 50, 4, '#1abc9c'),
    ('Phase 8: Deployment', 54, 2, '#e67e22'),
]

# Create bars for phases
y_pos = np.arange(len(phases))
for i, (phase, start, duration, color) in enumerate(phases):
    ax.barh(i, duration, left=start, height=0.7, 
            color=color, edgecolor='black', linewidth=1,
            alpha=0.85)
    
    # Add phase labels
    ax.text(0.5, i, phase, va='center', ha='right', fontsize=11, fontweight='bold')

# Customize axes
ax.set_yticks(y_pos)
ax.set_yticklabels([''] * len(phases))
ax.set_xlabel('Days', fontsize=12, fontweight='bold')
ax.set_title('AI-Powered College Chatbot - Project Gantt Chart (56 Days / 8 Weeks)', 
             fontsize=16, fontweight='bold', pad=20)

# Set x-axis to show weeks
ax.set_xticks(range(0, 50, 7))
ax.set_xticklabels([f'Week {i+1}' for i in range(8)])
ax.set_xlim(0, 56)

# Add grid
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add legend
legend_elements = [
    plt.Rectangle((0,0),1,1, fc='#3498db', alpha=0.85, label='Planning'),
    plt.Rectangle((0,0),1,1, fc='#9b59b6', alpha=0.85, label='Database'),
    plt.Rectangle((0,0),1,1, fc='#e74c3c', alpha=0.85, label='Backend Core'),
    plt.Rectangle((0,0),1,1, fc='#c0392b', alpha=0.85, label='Backend Advanced'),
    plt.Rectangle((0,0),1,1, fc='#2ecc71', alpha=0.85, label='Frontend'),
    plt.Rectangle((0,0),1,1, fc='#f39c12', alpha=0.85, label='Testing'),
    plt.Rectangle((0,0),1,1, fc='#1abc9c', alpha=0.85, label='Documentation'),
    plt.Rectangle((0,0),1,1, fc='#e67e22', alpha=0.85, label='Deployment'),
]
ax.legend(handles=legend_elements, loc='upper right', 
         framealpha=0.9, fontsize=10, ncol=2)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(left=0.25, right=0.95)

# Save the figure
plt.savefig('gantt_chart.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.savefig('gantt_chart.pdf', bbox_inches='tight', 
            facecolor='white', edgecolor='none')

print("✅ Gantt chart saved as 'gantt_chart.png' and 'gantt_chart.pdf'")
print("📊 Resolution: 300 DPI (high quality for documentation)")

# Display
plt.show()