import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import BalanceBlock from "../context/BalanceBlock";

const DashboardPage = () => {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUsername = localStorage.getItem("username");

    if (!token || !storedUsername) {
      navigate("/login");
      return;
    }

    setUsername(storedUsername);
  }, [navigate]);

  const token = localStorage.getItem("token");

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Welcome, {username}!</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <BalanceBlock token={token} username={username} />
      </div>
    </div>
  );
};

export default DashboardPage;
