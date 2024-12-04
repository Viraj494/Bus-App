import React, { useEffect, useState } from 'react';
import { StyleSheet } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { fetchBuses } from '../../services/firebaseService'; // Adjust path if necessary
import { MaterialIcons } from '@expo/vector-icons'; // Import MaterialIcons from @expo/vector-icons

// Function to calculate distance between two points (latitude/longitude) in kilometers
const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
  const R = 6371; // Earth radius in kilometers
  const dLat = (lat2 - lat1) * (Math.PI / 180);
  const dLon = (lon2 - lon1) * (Math.PI / 180);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * (Math.PI / 180)) *
      Math.cos(lat2 * (Math.PI / 180)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c; // Distance in kilometers
  return distance;
};

export default function MapScreen() {
  const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null); // Coordinates type
  const [buses, setBuses] = useState<Array<any>>([]); // Type buses data as an array of objects

  // Set Homagama's coordinates manually (user's current location)
  useEffect(() => {
    setLocation({
      latitude: 6.9300, // Homagama Latitude
      longitude: 79.9817, // Homagama Longitude
    });
  }, []);

  // Fetch buses data from Firebase Realtime Database
  useEffect(() => {
    const loadBuses = async () => {
      const data = await fetchBuses(); // Fetch buses from Firebase
      setBuses(data); // Store buses data
    };
    loadBuses(); // Load buses data when component mounts
  }, []);

  if (!location) return null; // Wait until location is set

  return (
    <MapView
      style={styles.map}
      initialRegion={{
        latitude: location.latitude,
        longitude: location.longitude,
        latitudeDelta: 0.0922,
        longitudeDelta: 0.0421,
      }}
    >
      {/* Marker for the user's location */}
      <Marker
        coordinate={{
          latitude: location.latitude,
          longitude: location.longitude,
        }}
        title="You"
      >
        {/* You can use custom marker icon here if needed */}
      </Marker>

      {/* Markers for each bus */}
      {buses.map((bus) => {
        const distance = calculateDistance(
          location.latitude,
          location.longitude,
          bus.location.latitude,
          bus.location.longitude
        );

        return (
          <Marker
            key={bus.id}
            coordinate={{
              latitude: bus.location.latitude,
              longitude: bus.location.longitude,
            }}
            title={`Route: ${bus.route}`}
            description={`ETA: ${bus.eta} mins, Distance: ${distance.toFixed(2)} km`}
          >
            {/* Custom icon for the bus */}
            <MaterialIcons name="directions-bus" size={40} color="blue" />
          </Marker>
        );
      })}
    </MapView>
  );
}

const styles = StyleSheet.create({
  map: {
    flex: 1,
  },
});
