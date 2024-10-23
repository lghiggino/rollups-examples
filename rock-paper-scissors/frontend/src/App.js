import { ethers } from "ethers";
import React, { useEffect, useState } from "react";
import "./App.css";
import CreateChallenge from './CreateChallenge';

// Simple App to present the Input field and produced Notices
function App() {
    const [signer, setSigner] = useState(undefined);

    useEffect(() => {
        if (window.ethereum === "undefined") {
            return alert("Please install MetaMask to use this dApp");
        }
        try {
            window.ethereum
                .request({ method: "eth_requestAccounts" })
                .then(() => {
                    const provider = new ethers.providers.Web3Provider(
                        window.ethereum
                    );
                    const signer = provider.getSigner();
                    setSigner(signer);
                })
                .catch((error) => {
                    throw error;
                });
        } catch (error) {
            console.error(error);
            alert("Connection with MetaMask failed");
        }
    }, []);

    return <div className="App">
        <CreateChallenge signer={signer} />
    </div>;
}

export default App;
