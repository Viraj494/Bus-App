// scripts/addBusesData.ts
import { ref, set } from "firebase/database";
import { database } from "../constants/firebaseConfig"; // Adjust the path as needed

/**
 * Add buses data to Firebase Realtime Database
 */
const addBusesData = async () => {
  try {
    const busesRef = ref(database, "buses"); // Reference to 'buses' collection

    const busesData = {
      bus1: {
        route: "101",
        location: {
          latitude: 37.7749,
          longitude: -122.4194,
        },
        eta: 10,
      },
      bus2: {
        route: "102",
        location: {
          latitude: 37.7849,
          longitude: -122.4094,
        },
        eta: 15,
      },
    };

    await set(busesRef, busesData);
    console.log("Buses data added successfully.");
  } catch (error) {
    console.error("Error adding buses data:", error);
  }
};

// Call the function to add data
addBusesData();
