"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, Label } from 'recharts';


/* Frame container holding the Recharts Line Graph */
export default function PNLDataChartFrame({ chartData, className }) {

  return (
    <div className={`w-full h-[400px] relative rounded-md border transition-colors ${className}`}>
      {/* Recharts Line Graph */}
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          width={500}
          height={300}
          data={chartData}
          margin={{
            top: 30,
            right: 30,
            left: 20,
            bottom: 0,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis/>
          <Tooltip />
          <Legend />
          <Line type="linear" dataKey="Historical" stroke="#8884d8" activeDot={{ r: 8 }} strokeLinecap="round" />
          <Line type="linear" dataKey="Forecasted" stroke="#d277f0ff" activeDot={{ r: 8 }} strokeLinecap="round" strokeDasharray="7 7" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
