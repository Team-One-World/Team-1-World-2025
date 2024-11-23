import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
        const res = await api.post(route, { username, password });
        if (method === "login") {
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
            navigate("/");
        } else {
            navigate("/login");
        }
    } catch (error) {
        alert(error);
    } finally {
        setLoading(false);
    }
};

  return (
    <form onSubmit={handleSubmit} className="flex flex-col space-y-4 px-4 py-8 mt-8 bg-gray-100 rounded-md shadow-md max-w-md mx-auto">
        <h1 className="text-2xl font-medium text-center">{name}</h1>
        <input
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:border-sky-500"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
        />
        <input
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:border-sky-500"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
        />
        {loading && <p className="text-center text-red-500">Loading...</p>}
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 rounded-md px-4" type="submit">
            {name}
        </button>
    </form>
  );
}

export default Form;