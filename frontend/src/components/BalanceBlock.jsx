import React, { useState, useEffect } from "react";

const BalanceBlock = ({ token, username }) => {
  const [balances, setBalances] = useState([]);
  const [newAccount, setNewAccount] = useState({
    account_type: "",
    balance: "",
    currency: "USD",
  });
  const [editAccount, setEditAccount] = useState(null);
  const [mainCurrency, setMainCurrency] = useState("USD");

  // Fetch balances from the backend
  useEffect(() => {
    const fetchBalances = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/balances/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setBalances(data);
      } catch (error) {
        console.error("Error fetching balances:", error);
      }
    };

    fetchBalances();
  }, [token]);

  // Add a new account
  const handleAddAccount = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/balances/add", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newAccount),
      });

      if (!response.ok) {
        throw new Error("Failed to add account");
      }

      setNewAccount({ account_type: "", balance: "", currency: "USD" });
      const data = await response.json();
      console.log(data.message);
      window.location.reload();
    } catch (error) {
      console.error("Error adding account:", error);
    }
  };

  // Update an account
  const handleUpdateAccount = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/balances/${id}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(editAccount),
      });

      if (!response.ok) {
        throw new Error("Failed to update account");
      }

      setEditAccount(null);
      const data = await response.json();
      console.log(data.message);
      window.location.reload();
    } catch (error) {
      console.error("Error updating account:", error);
    }
  };

  // Delete an account
  const handleDeleteAccount = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/balances/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to delete account");
      }

      const data = await response.json();
      console.log(data.message);
      window.location.reload();
    } catch (error) {
      console.error("Error deleting account:", error);
    }
  };

  return (
    <div className="bg-blue-100 p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold">Balance</h2>

      {/* Main Currency Selection */}
      <div className="mb-4">
        <label htmlFor="main-currency" className="block font-bold">
          Main Currency:
        </label>
        <select
          id="main-currency"
          value={mainCurrency}
          onChange={(e) => setMainCurrency(e.target.value)}
          className="border rounded px-2 py-1"
        >
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="KZT">KZT</option>
        </select>
      </div>

      {/* Balances List */}
      <ul className="list-disc pl-5">
        {balances.map((account) => (
          <li key={account.id}>
            {editAccount?.id === account.id ? (
              <div>
                <input
                  type="text"
                  value={editAccount.account_type}
                  onChange={(e) =>
                    setEditAccount({ ...editAccount, account_type: e.target.value })
                  }
                  className="border rounded px-2 py-1"
                />
                <input
                  type="number"
                  value={editAccount.balance}
                  onChange={(e) =>
                    setEditAccount({ ...editAccount, balance: e.target.value })
                  }
                  className="border rounded px-2 py-1 ml-2"
                />
                <select
                  value={editAccount.currency}
                  onChange={(e) =>
                    setEditAccount({ ...editAccount, currency: e.target.value })
                  }
                  className="border rounded px-2 py-1 ml-2"
                >
                  <option value="USD">USD</option>
                  <option value="EUR">EUR</option>
                  <option value="KZT">KZT</option>
                </select>
                <button
                  onClick={() => handleUpdateAccount(account.id)}
                  className="ml-2 bg-green-500 text-white px-2 py-1 rounded"
                >
                  Save
                </button>
              </div>
            ) : (
              <>
                {account.account_type}: {account.balance} {account.currency}{" "}
                (<span>
                  {account.converted_balances[mainCurrency]} {mainCurrency}
                </span>)
                <button
                  onClick={() => setEditAccount(account)}
                  className="ml-2 bg-yellow-500 text-white px-2 py-1 rounded"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDeleteAccount(account.id)}
                  className="ml-2 bg-red-500 text-white px-2 py-1 rounded"
                >
                  Delete
                </button>
              </>
            )}
          </li>
        ))}
      </ul>

      {/* Add Account Form */}
      <div className="bg-white p-4 rounded-lg shadow-md mt-4">
        <h3 className="text-lg font-bold">Add Account</h3>
        <input
          type="text"
          value={newAccount.account_type}
          onChange={(e) =>
            setNewAccount({ ...newAccount, account_type: e.target.value })
          }
          placeholder="Account Type"
          className="border rounded px-2 py-1 mr-2"
        />
        <input
          type="number"
          value={newAccount.balance}
          onChange={(e) =>
            setNewAccount({ ...newAccount, balance: e.target.value })
          }
          placeholder="Balance"
          className="border rounded px-2 py-1 mr-2"
        />
        <select
          value={newAccount.currency}
          onChange={(e) =>
            setNewAccount({ ...newAccount, currency: e.target.value })
          }
          className="border rounded px-2 py-1"
        >
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="KZT">KZT</option>
        </select>
        <button
          onClick={handleAddAccount}
          className="ml-2 bg-blue-500 text-white px-2 py-1 rounded"
        >
          Add
        </button>
      </div>
    </div>
  );
};

export default BalanceBlock;
