import { Button, Heading, Select, useToast } from "@chakra-ui/react";
import React, { useState } from "react";
import { generateCommitment, sendIput } from "./util";

export default function CreateChallenge({ signer }) {
    const [choice, setChoice] = useState("1");
    const [loading, setLoading] = useState(false);

    const toast = useToast();

    async function createChallenge() {
        const commitmet = await generateCommitment(choice, signer);
        await sendIput(
            JSON.stringify({
                method: "create_challenge",
                commitment: commitmet,
            }),
            signer,
            toast
        );
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setLoading(true);
        await createChallenge();
        setLoading(false);
    }

    let buttonProps = {};
    if (loading) buttonProps.isLoading = true;

    return (
        <div className="challengeForm">
            <form onSubmit={handleSubmit}>
                <Heading size="lg">Create Challenge</Heading>
                <div>
                    <label>
                        <p>Choice</p>
                    </label>
                    <Select
                        focusBorderColor="yellow"
                        size="md"
                        width={180}
                        value={choice}
                        onChange={(e) => setChoice(e.target.value)}
                    >
                        <option value={"1"}>ROCK</option>
                        <option value={"2"}>PAPER</option>
                        <option value={"3"}>SCISSORS</option>
                    </Select>
                </div>
                <Button
                    {...buttonProps}
                    type="submit"
                    colorScheme="blue"
                    isLoading={loading}
                >
                    Create Challenge
                </Button>
            </form>
        </div>
    );
}
