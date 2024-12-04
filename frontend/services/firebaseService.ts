import { getDatabase, ref, get } from "firebase/database";
import { app } from "../constants/firebaseConfig"; // Named import for the Firebase app instance

// Initialize the Realtime Database instance
let database;
try {
  database = getDatabase(app);
  console.log("Successfully connected to Firebase Realtime Database.");
} catch (error) {
  console.error("Error initializing Firebase Realtime Database:", error);
  throw new Error("Database initialization failed.");
}

/**
 * Fetches all buses from the Realtime Database
 * @returns {Promise<Array<Object>>} An array of bus objects
 */
export const fetchBuses = async () => {
  try {
    // Reference to the 'buses' collection in the Realtime Database
    const busesRef = ref(database, "buses");

    // Fetch data from the database
    const snapshot = await get(busesRef);

    if (snapshot.exists()) {
      // If data exists, convert the object into an array
      const buses = snapshot.val();
      console.log("Successfully fetched buses data:", buses);
      return Object.keys(buses).map((key) => ({
        id: key, // Add the bus key as 'id'
        ...buses[key], // Spread the rest of the bus data
      }));
    } else {
      console.warn("No data available in 'buses' collection.");
      return [];
    }
  } catch (error) {
    console.error("Error fetching buses data from Firebase:", error);
    return [];
  }
};
