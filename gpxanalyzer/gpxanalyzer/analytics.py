from gpxanalyzer.importer import read_gpx
import gpxpy

def haversine_distance(coord1, coord2):
    import math

    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371000  # Earth radius in meters
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

def overlapping_segments(gpx1, gpx2, threshold=10):
    overlap_distance = 0
    for track1 in gpx1.tracks:
        for segment1 in track1.segments:
            for point1, point2 in zip(segment1.points[:-1], segment1.points[1:]):
                for track2 in gpx2.tracks:
                    for segment2 in track2.segments:
                        for point3, point4 in zip(segment2.points[:-1], segment2.points[1:]):
                            if (haversine_distance((point1.latitude, point1.longitude), (point3.latitude, point3.longitude)) < threshold or
                                haversine_distance((point1.latitude, point1.longitude), (point4.latitude, point4.longitude)) < threshold or
                                haversine_distance((point2.latitude, point2.longitude), (point3.latitude, point3.longitude)) < threshold or
                                haversine_distance((point2.latitude, point2.longitude), (point4.latitude, point4.longitude)) < threshold):

                                overlap_distance += haversine_distance((point1.latitude, point1.longitude), (point2.latitude, point2.longitude))
    return overlap_distance

def compute_refined_overlapping_distance(gpx1, gpx2, threshold=10):
    """Compute overlapping distance between two GPX routes without over-counting."""
    
    # Extract latitudes and longitudes from the GPX objects
    gpx1_lat, gpx1_lon = [], []
    for track in gpx1.tracks:
        for segment in track.segments:
            for point in segment.points:
                gpx1_lat.append(point.latitude)
                gpx1_lon.append(point.longitude)
                
    gpx2_lat, gpx2_lon = [], []
    for track in gpx2.tracks:
        for segment in track.segments:
            for point in segment.points:
                gpx2_lat.append(point.latitude)
                gpx2_lon.append(point.longitude)
    
    overlap_distance = 0.0
    considered_segments = set()  # To keep track of segments that have been considered

    for i in range(len(gpx1_lat) - 1):
        for j in range(len(gpx2_lat) - 1):
            # Check if the segment in gpx1 overlaps with any point in gpx2
            if haversine_distance((gpx1_lat[i], gpx1_lon[i]), (gpx2_lat[j], gpx2_lon[j])) < threshold:
                if i not in considered_segments:
                    overlap_distance += haversine_distance((gpx1_lat[i], gpx1_lon[i]), (gpx1_lat[i + 1], gpx1_lon[i + 1]))
                    considered_segments.add(i)
                    
    return overlap_distance


def elevation_gain(gpx):
    gain = 0
    for track in gpx.tracks:
        for segment in track.segments:
            for point1, point2 in zip(segment.points[:-1], segment.points[1:]):
                if point2.elevation > point1.elevation:
                    gain += (point2.elevation - point1.elevation)
    return gain


def merge_gpx_files(gpx_objects, threshold=5):
    """
    Combine multiple GPX objects into a single continuous route.

    Parameters:
    - gpx_objects: List of GPX objects to be merged.
    - threshold: The distance threshold (in meters) to consider points as duplicate.

    Returns:
    - Combined GPX object.
    """
    combined_gpx = gpxpy.gpx.GPX()

    for gpx in gpx_objects:
        for track in gpx.tracks:
            new_track = gpxpy.gpx.GPXTrack()
            combined_gpx.tracks.append(new_track)

            new_segment = gpxpy.gpx.GPXTrackSegment()
            new_track.segments.append(new_segment)

            for segment in track.segments:
                for point in segment.points:
                    if not new_segment.points or haversine_distance(
                        (new_segment.points[-1].latitude, new_segment.points[-1].longitude),
                        (point.latitude, point.longitude)
                    ) > threshold:
                        new_segment.points.append(point)

    return combined_gpx