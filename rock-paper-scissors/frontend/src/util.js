import { InputBox__factory } from "@cartesi/rollups";
import { ethers } from "ethers";
import {
    DAPP_ADDRESS,
    INPUTBOX_ADDRESS,
    MOVE_KEY,
    NONCE_KEY,
} from "./constants";

export async function generateHash(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join();
    return hashHex;
}

export const generateCommitment = async (choice, signer) => {
    const address = await signer.getAddress();
    const nonce = Math.random() * 1000
    localStorage.setItem(NONCE_KEY + address.toLowerCase(), nonce);
    localStorage.setItem(MOVE_KEY + address.toLowerCase(), choice);

    const commitment = await generateHash(nonce.toString() + choice);
    return commitment;
};

export const sendIput = async (value, signer, toast) => {
    const inputBox = InputBox__factory.connect(INPUTBOX_ADDRESS, signer);
    const inputBytes = ethers.utils.isBytesLike(value)
        ? value
        : ethers.utils.toUtf8Bytes(value);
    const tx = await inputBox.addInput(DAPP_ADDRESS, inputBytes);

    return await waitForTransaction(tx, toast);
};

export const waitForTransaction = async (tx, toast) => {
    toast({
        "title": "Transaction sent",
        "description": "Waiting for confirmation",
        "status": "info",
        "duration": 9000,
        "isClosable": true,
        "position": "top-right",
    })

    const receipt = await tx.wait(1);
    const event = receipt.events?.find((event) => event.event === "InputAdded");
    console.log("@utils.waitForTransaction event", event.args);

    toast({
        "title": "Confirmed ",
        "description": `Input added => index: ${event?.args[1]?.inboxInputIndex}`,
        "status": "success",
        "duration": 9000,
        "isClosable": true,
        "position": "top-right",
    })

    return receipt;
}
