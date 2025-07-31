import React, { useEffect, useState } from "react";
import {
  View,
  FlatList,
  ActivityIndicator,
  Alert,
  TouchableOpacity,
} from "react-native";
import { Text, Card, Button } from "react-native-paper";
import axios from "axios";
import * as Location from "expo-location";
import { MaterialIcons } from "@expo/vector-icons";

const categories = [
  { name: "Bus Stops", type: "bus_station", icon: "directions-bus" },
  { name: "Restaurants", type: "restaurant", icon: "restaurant" },
  { name: "Hotels", type: "lodging", icon: "hotel" },
  { name: "Hospitals", type: "hospital", icon: "local-hospital" },
  { name: "Gas Stations", type: "gas_station", icon: "local-gas-station" },
];

const PlacesRecommendation = () => {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("bus_station");

  useEffect(() => {
    fetchPlaces(selectedCategory);
  }, [selectedCategory]);

  const fetchPlaces = async (category: string) => {
    setLoading(true);
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== "granted") {
      Alert.alert(
        "Permission Denied",
        "Allow location access to get recommendations."
      );
      setLoading(false);
      return;
    }

    const location = await Location.getCurrentPositionAsync({});
    const latitude = location.coords.latitude;
    const longitude = location.coords.longitude;

    try {
      const response = await axios.get(
        `http://your-backend-url/recommend-places`,
        {
          params: { latitude, longitude, category },
        }
      );
      setPlaces(response.data.places);
    } catch (error) {
      Alert.alert("Error", "Failed to fetch places.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ flex: 1, padding: 20, backgroundColor: "#f8f9fa" }}>
      <Text
        style={{
          fontSize: 24,
          fontWeight: "bold",
          textAlign: "center",
          marginBottom: 15,
        }}
      >
        Recommended Places
      </Text>

      {/* Category Selector */}
      <FlatList
        horizontal
        data={categories}
        keyExtractor={(item) => item.type}
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={{ marginBottom: 15 }}
        renderItem={({ item }) => (
          <TouchableOpacity
            onPress={() => setSelectedCategory(item.type)}
            style={{
              backgroundColor:
                selectedCategory === item.type ? "#007bff" : "#ddd",
              padding: 10,
              borderRadius: 20,
              marginHorizontal: 5,
              flexDirection: "row",
              alignItems: "center",
            }}
          >
            <MaterialIcons name={item.icon} size={20} color="white" />
            <Text style={{ color: "white", marginLeft: 5 }}>{item.name}</Text>
          </TouchableOpacity>
        )}
      />

      {loading ? (
        <ActivityIndicator size="large" color="#007bff" />
      ) : (
        <FlatList
          data={places}
          keyExtractor={(item) => item.name}
          renderItem={({ item }) => (
            <Card style={{ marginBottom: 10, padding: 10, borderRadius: 10 }}>
              <Card.Title
                title={item.name}
                subtitle={item.address}
                left={(props) => (
                  <MaterialIcons
                    {...props}
                    name="place"
                    size={30}
                    color="#007bff"
                  />
                )}
              />
              <Card.Content>
                <Text style={{ fontSize: 16, fontWeight: "bold" }}>
                  Rating: {item.rating}
                </Text>
              </Card.Content>
              <Card.Actions>
                <Button
                  mode="contained"
                  onPress={() => Alert.alert("Selected Place", item.name)}
                >
                  View Details
                </Button>
              </Card.Actions>
            </Card>
          )}
        />
      )}
    </View>
  );
};

export default PlacesRecommendation;
