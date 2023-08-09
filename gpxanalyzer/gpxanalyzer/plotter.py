import matplotlib.pyplot as plt
from gpxanalyzer.analytics import overlapping_segments, haversine_distance
import folium

def plot_tracks_with_overlap(gpx1, gpx2, threshold=10):
    plt.figure(figsize=(10, 6))

    # Plot Track 1 (non-overlapping)
    for track in gpx1.tracks:
        for segment in track.segments:
            latitudes = [point.latitude for point in segment.points]
            longitudes = [point.longitude for point in segment.points]

            overlap_lats, overlap_longs = [], []
            unique_lats, unique_longs = [], []
            for lat, long in zip(latitudes, longitudes):
                if any(haversine_distance((lat, long), (p.latitude, p.longitude)) < threshold for t in gpx2.tracks for s in t.segments for p in s.points):
                    if unique_lats and unique_longs:
                        plt.plot(unique_longs, unique_lats, 'b-')
                        unique_lats, unique_longs = [], []
                    overlap_lats.append(lat)
                    overlap_longs.append(long)
                else:
                    if overlap_lats and overlap_longs:
                        plt.plot(overlap_longs, overlap_lats, 'g-')
                        overlap_lats, overlap_longs = [], []
                    unique_lats.append(lat)
                    unique_longs.append(long)

            if overlap_lats and overlap_longs:
                plt.plot(overlap_longs, overlap_lats, 'g-')
            if unique_lats and unique_longs:
                plt.plot(unique_longs, unique_lats, 'b-')

    # Plot Track 2 (non-overlapping)
    for track in gpx2.tracks:
        for segment in track.segments:
            latitudes = [point.latitude for point in segment.points]
            longitudes = [point.longitude for point in segment.points]

            overlap_lats, overlap_longs = [], []
            unique_lats, unique_longs = [], []
            for lat, long in zip(latitudes, longitudes):
                if any(haversine_distance((lat, long), (p.latitude, p.longitude)) < threshold for t in gpx1.tracks for s in t.segments for p in s.points):
                    if unique_lats and unique_longs:
                        plt.plot(unique_longs, unique_lats, 'r-')
                        unique_lats, unique_longs = [], []
                    overlap_lats.append(lat)
                    overlap_longs.append(long)
                else:
                    if overlap_lats and overlap_longs:
                        plt.plot(overlap_longs, overlap_lats, 'g-')
                        overlap_lats, overlap_longs = [], []
                    unique_lats.append(lat)
                    unique_longs.append(long)

            if overlap_lats and overlap_longs:
                plt.plot(overlap_longs, overlap_lats, 'g-')
            if unique_lats and unique_longs:
                plt.plot(unique_longs, unique_lats, 'r-')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Tracks Overlay')
    blue_patch = plt.Line2D([], [], color='blue', label='Track 1 Only')
    red_patch = plt.Line2D([], [], color='red', label='Track 2 Only')
    green_patch = plt.Line2D([], [], color='green', label='Overlap')
    plt.legend(handles=[blue_patch, red_patch, green_patch])
    plt.show()



def plot_tracks_with_overlap_on_map(gpx1, gpx2, threshold=10):
    # Take the average latitude and longitude to center the map
    avg_lat = (gpx1.tracks[0].segments[0].points[0].latitude + gpx2.tracks[0].segments[0].points[0].latitude) / 2
    avg_lon = (gpx1.tracks[0].segments[0].points[0].longitude + gpx2.tracks[0].segments[0].points[0].longitude) / 2
    
    # Create a folium map with satellite view
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=15, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr="Esri")
    
    # Helper to add segments to map
    def add_to_map(segment, color):
        if isinstance(segment[0], tuple):
            latlng = segment
        else:
            latlng = [(point.latitude, point.longitude) for point in segment]
        folium.PolyLine(latlng, color=color).add_to(m)

    # Plotting logic similar to before but using add_to_map helper
    for gpx, color in zip([gpx1, gpx2], ['blue', 'red']):
        for track in gpx.tracks:
            for segment in track.segments:
                latitudes = [point.latitude for point in segment.points]
                longitudes = [point.longitude for point in segment.points]
                
                overlap_points, unique_points = [], []
                for lat, long in zip(latitudes, longitudes):
                    other_gpx = gpx2 if gpx == gpx1 else gpx1
                    if any(haversine_distance((lat, long), (p.latitude, p.longitude)) < threshold for t in other_gpx.tracks for s in t.segments for p in s.points):
                        if unique_points:
                            add_to_map(unique_points, color)
                            unique_points = []
                        overlap_points.append((lat, long))
                    else:
                        if overlap_points:
                            add_to_map(overlap_points, 'green')
                            overlap_points = []
                        unique_points.append((lat, long))
                
                if overlap_points:
                    add_to_map(overlap_points, 'green')
                if unique_points:
                    add_to_map(unique_points, color)
    
    # Display the map
    return m


def plot_gpx_on_map(gpx):
    """
    Plot a GPX object on a folium map.

    Parameters:
    - gpx: The GPX object to be plotted.

    Returns:
    - folium Map object.
    """
    # Extract the first point to center the map
    first_point = gpx.tracks[0].segments[0].points[0]
    m = folium.Map(location=[first_point.latitude, first_point.longitude], zoom_start=13, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr="Esri")

    for track in gpx.tracks:
        for segment in track.segments:
            latlng = [(point.latitude, point.longitude) for point in segment.points]
            folium.PolyLine(latlng, color="blue").add_to(m)

    return m