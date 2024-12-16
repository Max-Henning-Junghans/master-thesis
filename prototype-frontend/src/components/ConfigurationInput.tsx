import React, { useState } from "react";
import { Button, Form } from "react-bootstrap";

function ConfigurationInput() {
    const [fileContent, setFileContent] = useState<string | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                setFileContent(e.target?.result as string);
            };
            reader.readAsText(file);
        }
    };

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        if (fileContent) {
            try {
                const response = await fetch("/definitions", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: fileContent,
                });
                const result = response.ok;
                console.log("Response:", result);
            } catch (error) {
                console.error("Error submitting file content:", error);
            }
        }
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group>
                <Form.Control
                    type="file"
                    accept=".json"
                    onChange={handleFileChange}
                />
            </Form.Group>
            <Button type="submit" disabled={!fileContent}>Submit</Button>
        </Form>
    );
}

export default ConfigurationInput;
