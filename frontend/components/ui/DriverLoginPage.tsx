import React from "react";
import { View, Text, TextInput, Button, Alert } from "react-native";
import { useForm, Controller } from "react-hook-form";
import axios from "axios";

const DriverLogin = () => {
  const { control, handleSubmit, reset } = useForm();

  const onSubmit = async (data: any) => {
    try {
      const response = await axios.post(
        "http://your-backend-url/login-driver",
        data
      );
      Alert.alert("Success", response.data.message);
    } catch (error: any) {
      Alert.alert("Error", error.response?.data?.detail || "Login failed");
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 20, fontWeight: "bold", marginBottom: 10 }}>
        Bus Driver Login
      </Text>

      <Controller
        control={control}
        name="email"
        rules={{ required: true }}
        render={({ field }) => (
          <TextInput
            placeholder="Email"
            keyboardType="email-address"
            {...field}
            style={{ borderBottomWidth: 1, marginBottom: 10 }}
          />
        )}
      />

      <Controller
        control={control}
        name="password"
        rules={{ required: true }}
        render={({ field }) => (
          <TextInput
            placeholder="Password"
            secureTextEntry
            {...field}
            style={{ borderBottomWidth: 1, marginBottom: 10 }}
          />
        )}
      />

      <Button title="Login" onPress={handleSubmit(onSubmit)} />
    </View>
  );
};

export default DriverLogin;
