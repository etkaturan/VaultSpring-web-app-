import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div className="bg-gray-100 min-h-screen flex flex-col items-center justify-center">
      {/* Hero Section */}
      <div className="text-center max-w-3xl p-6 bg-white shadow-lg rounded-lg">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">Welcome to VaultSpring</h1>
        <p className="text-lg text-gray-600 mb-6">
          Your all-in-one intelligent financial management solution. Track balances, set financial goals, and gain valuable insights into your finances.
        </p>
        {/* Buttons */}
        <div className="flex space-x-4 justify-center">
          <Link
            to="/login"
            className="bg-blue-500 text-white px-6 py-3 rounded-md text-lg hover:bg-blue-600 transition"
          >
            Login
          </Link>
          <Link
            to="/register"
            className="bg-green-500 text-white px-6 py-3 rounded-md text-lg hover:bg-green-600 transition"
          >
            Register
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 px-6">
        {/* Feature 1 */}
        <div className="flex flex-col items-center text-center p-6 bg-white shadow rounded-lg">
          <div className="text-blue-500 text-4xl mb-4">
            <i className="fas fa-wallet"></i>
          </div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Track Balances</h2>
          <p className="text-gray-600">
            Keep an eye on your cash, bank accounts, and investments all in one place.
          </p>
        </div>

        {/* Feature 2 */}
        <div className="flex flex-col items-center text-center p-6 bg-white shadow rounded-lg">
          <div className="text-green-500 text-4xl mb-4">
            <i className="fas fa-bullseye"></i>
          </div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Set Goals</h2>
          <p className="text-gray-600">
            Define and achieve your financial goals with step-by-step progress tracking.
          </p>
        </div>

        {/* Feature 3 */}
        <div className="flex flex-col items-center text-center p-6 bg-white shadow rounded-lg">
          <div className="text-purple-500 text-4xl mb-4">
            <i className="fas fa-chart-line"></i>
          </div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Gain Insights</h2>
          <p className="text-gray-600">
            Analyze your spending patterns and get personalized financial insights.
          </p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
