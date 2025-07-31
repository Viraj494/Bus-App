import React from "react";
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
} from "react-native";
import MapView, { Marker } from "react-native-maps";

const HelloWave = () => {
  const buses = [
    { id: "1", name: "Bus 101", latitude: 37.7749, longitude: -122.4194 },
    { id: "2", name: "Bus 102", latitude: 37.7755, longitude: -122.4183 },
    { id: "3", name: "Bus 103", latitude: 37.776, longitude: -122.4172 },
    { id: "4", name: "Bus 104", latitude: 37.7771, longitude: -122.4161 },
    { id: "5", name: "Bus 105", latitude: 37.7782, longitude: -122.415 },
    { id: "6", name: "Bus 106", latitude: 37.7793, longitude: -122.414 },
    { id: "7", name: "Bus 107", latitude: 37.7804, longitude: -122.413 },
    { id: "8", name: "Bus 108", latitude: 37.7815, longitude: -122.412 },
    { id: "9", name: "Bus 109", latitude: 37.7826, longitude: -122.411 },
    { id: "10", name: "Bus 110", latitude: 37.7837, longitude: -122.41 },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Bus Tracking System</Text>
      <MapView
        style={styles.map}
        initialRegion={{
          latitude: 37.7749,
          longitude: -122.4194,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        }}
      >
        {buses.map((bus) => (
          <Marker
            key={bus.id}
            coordinate={{ latitude: bus.latitude, longitude: bus.longitude }}
            title={bus.name}
          />
        ))}
      </MapView>
      <FlatList
        data={buses}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.busItem}>
            <Text style={styles.busText}>{item.name}</Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: {
    fontSize: 24,
    fontWeight: "bold",
    textAlign: "center",
    marginVertical: 10,
  },
  map: { flex: 1 },
  busItem: { padding: 15, borderBottomWidth: 1, borderBottomColor: "#ccc" },
  busText: { fontSize: 18 },
});

export default HelloWave;
