"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, Label } from 'recharts';

/* Frame container holding the Recharts Line Graph */
export default function KPIChartFrame({ chartData, chartTargetValue, className }) {

  console.log("chartData from KPIChartFrame:", chartData);
  console.log("chartTarget from KPIChartFrame:", chartTargetValue);

  // Safety checks - return early if data isn't ready
  if (!chartData || chartData.length === 0 || chartTargetValue === undefined || chartTargetValue === null) {
    return (
      <div className={`w-full h-[400px] relative rounded-md border transition-colors ${className} flex items-center justify-center`}>
        <p className="text-gray-500">Loading chart data...</p>
      </div>
    );
  }

  // Calculate the actual data range (excluding null values)
  const dataValues = chartData.flatMap(d => [d.Historical, d.Forecasted]).filter(v => v !== null && v !== undefined);
  
  if (dataValues.length === 0) {
    return (
      <div className={`w-full h-[400px] relative rounded-md border transition-colors ${className} flex items-center justify-center`}>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const dataMin = Math.min(...dataValues);
  const dataMax = Math.max(...dataValues);

  // Determine if target is within reasonable range (0.95x to 1.05x of data range)
  const rangeMin = dataMin * (dataMin < 0 ? 1.05 : 0.95);
  const rangeMax = dataMax * (dataMax < 0 ? 0.95 : 1.05);
  
  const isTargetOutOfRange = chartTargetValue < rangeMin || chartTargetValue > rangeMax;
  
  // Calculate the effective Y-axis domain
  const yAxisMin = dataMin < 0 ? dataMin * 1.05 : dataMin * 0.95;
  const yAxisMax = dataMax < 0 ? dataMax * 0.95 : dataMax * 1.05;

  // Position target at top or bottom if out of range
  let effectiveTargetPosition = chartTargetValue;
  let targetLabel = `Target: ${chartTargetValue.toLocaleString()}`;
  
  if (isTargetOutOfRange) {
    if (chartTargetValue > rangeMax) {
      effectiveTargetPosition = yAxisMax;
      targetLabel = `Target: ${chartTargetValue.toLocaleString()} ↑`;
    } else if (chartTargetValue < rangeMin) {
      effectiveTargetPosition = yAxisMin;
      targetLabel = `Target: ${chartTargetValue.toLocaleString()} ↓`;
    }
  }

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
            domain={[yAxisMin, yAxisMax]}
            tickFormatter={(value) => value.toFixed(2)}
          />
          <Tooltip />
          <Legend />

          <ReferenceLine 
            y={effectiveTargetPosition} 
            stroke="red" 
            strokeOpacity={isTargetOutOfRange ? 0.5 : 0.7} 
            strokeDasharray="7 7"
          >
            <Label 
              value={targetLabel} 
              position="insideRight"
              style={{ fontWeight: isTargetOutOfRange ? 'bold' : 'normal' }}
            />
          </ReferenceLine>
          <Line type="linear" dataKey="Historical" stroke="#8884d8" activeDot={{ r: 8 }} strokeLinecap="round" />
          <Line type="linear" dataKey="Forecasted" stroke="#d277f0ff" activeDot={{ r: 8 }} strokeLinecap="round" strokeDasharray="7 7" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}