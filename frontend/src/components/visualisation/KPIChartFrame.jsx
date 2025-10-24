"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, Label } from 'recharts';


/* Frame container holding the Recharts Line Graph */
export default function KPIChartFrame({ chartData, chartTargetValue, className }) {

  console.log("chartData from KPIChartFrame:", chartData);
  console.log("chartTarget from KPIChartFrame:", chartTargetValue);
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
            right: 20,
            left: 45,
            bottom: 0,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis
            domain={
              [
                (dataMin) => {
                  const min = Math.min(dataMin, chartTargetValue);
                  // If negative, multiply by 1.05 to go more negative, if positive multiply by 0.95
                  return min < 0 ? min * 1.05 : min * 0.95;
                },
                (dataMax) => {
                  const max = Math.max(dataMax, chartTargetValue);
                  // If negative, multiply by 0.95 to go less negative, if positive multiply by 1.05
                  return max < 0 ? max * 0.95 : max * 1.05;
                }
              ]
            }
            tickFormatter={(value) => value.toFixed(2)}
          />
          <Tooltip />
          <Legend />

          <ReferenceLine y={chartTargetValue} stroke="red" strokeOpacity="0.7" strokeDasharray="7 7">
            <Label value={`Target: ${chartTargetValue.toLocaleString()}`} position="insideRight" />
          </ReferenceLine>
          <Line type="linear" dataKey="Historical" stroke="#8884d8" activeDot={{ r: 8 }} strokeLinecap="round" />
          <Line type="linear" dataKey="Forecasted" stroke="#d277f0ff" activeDot={{ r: 8 }} strokeLinecap="round" strokeDasharray="7 7" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
