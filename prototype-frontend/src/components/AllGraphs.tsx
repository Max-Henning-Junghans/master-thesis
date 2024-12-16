import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import SingleGraph from "./SingleGraph";

interface MeasurementData {
    [key: string]: [number, number][];
}

function AllGraphs() {
    const [data, setData] = useState<MeasurementData>({});
    const [loading, setLoading] = useState<boolean>(true);

    const fetchData = async () => {
        setLoading(true);
        try {
            const response = await fetch("/measurements");
            const result: MeasurementData = await response.json();
            setData(result);
        } catch (error) {
            console.error("Error fetching data:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            <div className="d-flex justify-content-center mb-3">
                <Button onClick={fetchData} disabled={loading}>
                    {loading ? "Loading..." : "Refresh Data"}
                </Button>
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "10px", justifyContent: "center", minHeight: "300px" }}>
                {Object.keys(data).map((name) => (
                    <SingleGraph key={name} name={name} measurements={data[name]} />
                ))}
            </div>
        </div>
    );
}

export default AllGraphs;
