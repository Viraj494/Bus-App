// Import Firebase app and Realtime Database functions
import { initializeApp, getApps, getApp } from "firebase/app";
import { getDatabase } from "firebase/database";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDVZA6iWZMiOh2v6HjafGhJKVsIi_PpBOo",
  authDomain: "busdata-4b1ce.firebaseapp.com",
  databaseURL: "https://busdata-4b1ce-default-rtdb.asia-southeast1.firebasedatabase.app/",
  projectId: "busdata-4b1ce",
  storageBucket: "busdata-4b1ce.appspot.com",
  messagingSenderId: "409752741165",
  appId: "1:409752741165:web:116d4c729e825e5e0f1fa4",
};

// Ensure only one Firebase app instance is initialized
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();

// Initialize and export the Realtime Database instance
const database = getDatabase(app);
export { app, database };
