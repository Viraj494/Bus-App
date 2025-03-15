import React, { useEffect, useState } from "react";
import { View, Text, FlatList, ActivityIndicator, Alert } from "react-native";
import axios from "axios";
import * as Location from "expo-location";

const PlacesRecommendation = () => {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPlaces = async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        Alert.alert(
          "Permission Denied",
          "Allow location access to get recommendations."
        );
        return;
      }

      const location = await Location.getCurrentPositionAsync({});
      const latitude = location.coords.latitude;
      const longitude = location.coords.longitude;

      try {
        const response = await axios.get(
          `http://your-backend-url/recommend-places`,
          {
            params: { latitude, longitude, category: "bus_station" },
          }
        );
        setPlaces(response.data.places);
      } catch (error) {
        Alert.alert("Error", "Failed to fetch places.");
      } finally {
        setLoading(false);
      }
    };

    fetchPlaces();
  }, []);

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 20, fontWeight: "bold", marginBottom: 10 }}>
        Recommended Places
      </Text>

      {loading ? (
        <ActivityIndicator size="large" color="blue" />
      ) : (
        <FlatList
          data={places}
          keyExtractor={(item) => item.name}
          renderItem={({ item }) => (
            <View style={{ padding: 10, borderBottomWidth: 1 }}>
              <Text style={{ fontSize: 16, fontWeight: "bold" }}>
                {item.name}
              </Text>
              <Text>{item.address}</Text>
              <Text>Rating: {item.rating}</Text>
            </View>
          )}
        />
      )}
    </View>
  );
};

export default PlacesRecommendation;
