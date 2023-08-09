#%%
from gpxanalyzer import importer, analytics, plotter

#%%
gpx1 = importer.read_gpx('spartan.gpx')
gpx2 = importer.read_gpx('tamalpa.gpx')

#%%
overlap_dist = analytics.overlapping_segments(gpx1, gpx2)

overlap_dist = analytics.compute_refined_overlapping_distance(gpx1, gpx2)
print(f"Overlapping Distance: {overlap_dist} meters")

gain1 = analytics.elevation_gain(gpx1)
gain2 = analytics.elevation_gain(gpx2)
print(f"Elevation Gain for Track 1: {gain1} meters")
print(f"Elevation Gain for Track 2: {gain2} meters")

plotter.plot_tracks_with_overlap(gpx1, gpx2)

# %%
map_result = plotter.plot_tracks_with_overlap_on_map(gpx1, gpx2)
map_result

# %%
gpx_objects = importer.load_gpx_files_from_directory("gpx_routes")
combined_gpx = analytics.merge_gpx_files(gpx_objects)
# %%
map_view = plotter.plot_gpx_on_map(combined_gpx)
map_view