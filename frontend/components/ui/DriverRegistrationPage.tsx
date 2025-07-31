import React from "react";
import { View, Text, TextInput, Button, Alert } from "react-native";
import { useForm, Controller } from "react-hook-form";
import axios from "axios";

const DriverRegister = () => {
    const { control, handleSubmit, reset } = useForm();

    const onSubmit = async (data: any) => {
        try {
            const response = await axios.post("http://your-backend-url/register-driver", data);
            Alert.alert("Success", response.data.message);
            reset();
        } catch (error: any) {
            Alert.alert("Error", error.response?.data?.detail || "Registration failed");
        }
    };

    return (
        <View style={{ padding: 20 }}>
            <Text style={{ fontSize: 20, fontWeight: "bold", marginBottom: 10 }}>Bus Driver Registration</Text>

            <Controller
                control={control}
                name="full_name"
                rules={{ required: true }}
                render={({ field }) => <TextInput placeholder="Full Name" {...field} style={{ borderBottomWidth: 1, marginBottom: 10 }} />}
            />
            
            <Controller
                control={control}
                name="license_number"
                rules={{ required: true }}
                render={({ field }) => <TextInput placeholder="License Number" {...field} style={{ borderBottomWidth: 1, marginBottom: 10 }} />}
            />

            <Controller
                control={control}
                name="phone_number"
                rules={{ required: true }}
                render={({ field }) => <TextInput placeholder="Phone Number" keyboardType="phone-pad" {...field} style={{ borderBottomWidth: 1, marginBottom: 10 }} />}
            />

            <Controller
                control={control}
                name="email"
                rules={{ required: true }}
                render={({ field }) => <TextInput placeholder="Email" keyboardType="email-address" {...field} style={{ borderBottomWidth: 1, marginBottom: 10 }} />}
            />

            <Controller
                control={control}
                name="password"
                rules={{ required: true }}
                render={({ field }) => <TextInput placeholder="Password" secureTextEntry {...field} style={{ borderBottomWidth: 1, marginBottom: 10 }} />}
            />

            <Controller
                control={control}
                name="bus_id"
                rules={{ required: true }}
                render={({ field }) => <TextInput placeholder="Bus ID" keyboardType="numeric" {...field} style={{ borderBottomWidth: 1, marginBottom: 10 }} />}
            />

            <Button title="Register" onPress={handleSubmit(onSubmit)} />
        </View>
    );
};

export default DriverRegister;
