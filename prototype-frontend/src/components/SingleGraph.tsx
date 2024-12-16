import React from "react";
import { Card } from "react-bootstrap";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface GraphProps {
    measurements: [number, number][];
    name: string;
}

function SingleGraph(props: GraphProps) {
    const data = {
        labels: props.measurements.map(measurement => {
            const date = new Date(measurement[0] * 1000); // Convert seconds to milliseconds
            return date.toLocaleString();
        }),
        datasets: [
            {
                label: `${props.name}`,
                data: props.measurements.map(measurement => measurement[1]),
                borderColor: "rgba(75,192,192,1)",
                backgroundColor: "rgba(75,192,192,0.2)",
            }
        ]
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: "top" as const,
            },
            title: {
                display: true,
                text: "Measurement Graph",
            },
        },
    };

    return (
        <Card style={{ minWidth: "600px", minHeight: "200px", margin: "10px" }}>
            <Card.Body style={{ minWidth: "600px", minHeight: "300px"}}>
                <Line data={data} options={options} />
            </Card.Body>
        </Card>
    );
}

export default SingleGraph;
