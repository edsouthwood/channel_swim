import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
# import cartopy.feature as cfeature
from cartopy.io.img_tiles import GoogleTiles
import numpy as np

# some extra variables
zoom = 0.1

# Load the CSV file
file_path = './boat.csv'
data = pd.read_csv(file_path)

# Ensure the data is sorted by timestamp
data = data.sort_values(by='Date/Time')

# Create the figure and axis for the plot
fig = plt.figure(figsize=(10, 10))

tiler = GoogleTiles(style="satellite")
ax = plt.axes(projection=tiler.crs)

# Add the Google Tiles
ax.add_image(tiler, 10)  # The second parameter is the zoom level, you can adjust it as needed


# for cfeature
# ax = plt.axes(projection=ccrs.PlateCarree())



# Add features to the map
# ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.OCEAN)
# ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(cfeature.BORDERS, linestyle=':')

# Set up plot limits and labels
# ax.set_extent([data['Longitude'].min() - zoom, data['Longitude'].max() + zoom, 
#               data['Latitude'].min() - zoom, data['Latitude'].max() + zoom])
ax.set_extent([data['Longitude'].min() - zoom, data['Longitude'].max() + zoom, 
               data['Latitude'].min() - zoom, data['Latitude'].max() + zoom], crs=ccrs.PlateCarree())
ax.set_title('Channel swim 11th July 2024')

# Initialize the scatter plot
scat = ax.scatter([], [], c='blue', edgecolor='k', transform=ccrs.PlateCarree())

# Initialize the timestamp text
timestamp_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')

# Initialize the animation
def init():
    scat.set_offsets(np.array([[], []]).T)
    timestamp_text.set_text('')
    return scat, timestamp_text

# Update the scatter plot and timestamp for each frame
def update(frame):
    offsets = data[['Longitude', 'Latitude']].iloc[:frame].to_numpy()
    scat.set_offsets(offsets)
    current_time = data['Date/Time'].iloc[frame]
    timestamp_text.set_text(f'Time: {current_time}')
    return scat, timestamp_text

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True)

# Save or display the animation
ani.save('boat_trip_animation.mp4', writer='ffmpeg', fps=2)
# plt.show()
