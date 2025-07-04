import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  AreaChart,
  Area,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';

// Color palettes for charts
const COLORS = {
  default: ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1'],
  business: ['#2563eb', '#16a34a', '#dc2626', '#ca8a04', '#9333ea'],
  modern: ['#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
  professional: ['#1f2937', '#374151', '#6b7280', '#9ca3af', '#d1d5db']
};

// Enhanced Bar Chart Component
export const EnhancedBarChart = ({ data, config, title }) => {
  const { xAxisKey, yAxisKey, barColor = '#8884d8' } = config;
  
  return (
    <div className="w-full h-full">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">{title}</h3>
      <ResponsiveContainer width="100%" height="85%">
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey={xAxisKey} 
            angle={-45}
            textAnchor="end"
            height={80}
            fontSize={12}
          />
          <YAxis fontSize={12} />
          <Tooltip 
            formatter={(value, name) => [value.toLocaleString(), name]}
            labelFormatter={(label) => `${xAxisKey}: ${label}`}
          />
          <Bar dataKey={yAxisKey} fill={barColor} radius={[4, 4, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS.modern[index % COLORS.modern.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

// Enhanced Line Chart Component
export const EnhancedLineChart = ({ data, config, title }) => {
  const { xAxisKey, yAxisKey, lineColor = '#8884d8' } = config;
  
  return (
    <div className="w-full h-full">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">{title}</h3>
      <ResponsiveContainer width="100%" height="85%">
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xAxisKey} fontSize={12} />
          <YAxis fontSize={12} />
          <Tooltip 
            formatter={(value, name) => [value.toLocaleString(), name]}
            labelFormatter={(label) => `${xAxisKey}: ${label}`}
          />
          <Line 
            type="monotone" 
            dataKey={yAxisKey} 
            stroke={lineColor} 
            strokeWidth={3}
            dot={{ fill: lineColor, strokeWidth: 2, r: 6 }}
            activeDot={{ r: 8, stroke: lineColor, strokeWidth: 2 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

// Enhanced Pie Chart Component
export const EnhancedPieChart = ({ data, config, title }) => {
  const { nameKey, valueKey, colors = COLORS.modern } = config;
  
  const RADIAN = Math.PI / 180;
  const renderCustomizedLabel = ({
    cx, cy, midAngle, innerRadius, outerRadius, percent, index
  }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };
  
  return (
    <div className="w-full h-full">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">{title}</h3>
      <ResponsiveContainer width="100%" height="85%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderCustomizedLabel}
            outerRadius={100}
            fill="#8884d8"
            dataKey={valueKey}
            nameKey={nameKey}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value, name) => [value.toLocaleString(), name]} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

// Enhanced Area Chart Component
export const EnhancedAreaChart = ({ data, config, title }) => {
  const { xAxisKey, yAxisKey, areaColor = '#8884d8' } = config;
  
  return (
    <div className="w-full h-full">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">{title}</h3>
      <ResponsiveContainer width="100%" height="85%">
        <AreaChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xAxisKey} fontSize={12} />
          <YAxis fontSize={12} />
          <Tooltip 
            formatter={(value, name) => [value.toLocaleString(), name]}
            labelFormatter={(label) => `${xAxisKey}: ${label}`}
          />
          <Area 
            type="monotone" 
            dataKey={yAxisKey} 
            stroke={areaColor}
            fill={areaColor}
            fillOpacity={0.6}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

// Enhanced Scatter Chart Component
export const EnhancedScatterChart = ({ data, config, title }) => {
  const { xAxisKey, yAxisKey, dotColor = '#8884d8' } = config;
  
  return (
    <div className="w-full h-full">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">{title}</h3>
      <ResponsiveContainer width="100%" height="85%">
        <ScatterChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xAxisKey} fontSize={12} />
          <YAxis dataKey={yAxisKey} fontSize={12} />
          <Tooltip 
            formatter={(value, name) => [value.toLocaleString(), name]}
            labelFormatter={(label) => `Point: ${label}`}
          />
          <Scatter name="Data Points" data={data} fill={dotColor} />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

// Chart Renderer Component
export const ChartRenderer = ({ chartConfig, className = "" }) => {
  console.log('ChartRenderer received:', chartConfig);
  
  if (!chartConfig || !chartConfig.type) {
    console.log('No chart config or type');
    return (
      <div className={`flex items-center justify-center h-64 bg-gray-100 rounded-lg ${className}`}>
        <p className="text-gray-500">No chart data available</p>
      </div>
    );
  }

  const { type, data, title, config } = chartConfig;
  
  console.log('Chart type:', type, 'Data length:', data?.length);

  if (!data || !Array.isArray(data) || data.length === 0) {
    return (
      <div className={`flex items-center justify-center h-64 bg-gray-100 rounded-lg ${className}`}>
        <p className="text-gray-500">No data available for chart</p>
      </div>
    );
  }

  const chartProps = {
    data,
    config,
    title
  };

  switch (type) {
    case 'bar':
      return <EnhancedBarChart {...chartProps} />;
    case 'line':
      return <EnhancedLineChart {...chartProps} />;
    case 'pie':
      return <EnhancedPieChart {...chartProps} />;
    case 'area':
      return <EnhancedAreaChart {...chartProps} />;
    case 'scatter':
      return <EnhancedScatterChart {...chartProps} />;
    default:
      console.log('Unknown chart type:', type, 'using bar chart');
      return <EnhancedBarChart {...chartProps} />;
  }
};

// Dashboard Grid Component
export const DashboardGrid = ({ dashboardConfig }) => {
  if (!dashboardConfig || !dashboardConfig.charts) {
    return (
      <div className="text-center p-8">
        <h3 className="text-lg font-semibold text-gray-700 mb-2">No Dashboard Available</h3>
        <p className="text-gray-500">Ask AI to create a dashboard for your data</p>
      </div>
    );
  }

  return (
    <div className="w-full p-4">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
        {dashboardConfig.title || 'Data Dashboard'}
      </h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {dashboardConfig.charts.map((chart, index) => (
          <div
            key={chart.id || index}
            className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 h-96"
          >
            <ChartRenderer chartConfig={chart.config} />
          </div>
        ))}
      </div>
    </div>
  );
};

// Chart Suggestion Component
export const ChartSuggestion = ({ suggestion, onCreateChart }) => {
  if (!suggestion) return null;

  const { recommended_chart, suggestions } = suggestion;

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
      <h4 className="font-semibold text-blue-900 mb-2">📊 Chart Recommendations</h4>
      
      {recommended_chart && (
        <div className="mb-3">
          <div className="flex items-center justify-between">
            <div>
              <span className="font-medium text-blue-800">
                Recommended: {recommended_chart.chart_type.toUpperCase()} Chart
              </span>
              <p className="text-sm text-blue-600 mt-1">{recommended_chart.reason}</p>
            </div>
            <button
              onClick={() => onCreateChart(recommended_chart)}
              className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              Create Chart
            </button>
          </div>
        </div>
      )}

      {suggestions?.recommended_charts && suggestions.recommended_charts.length > 1 && (
        <div>
          <p className="text-xs font-medium text-blue-700 mb-2">Other Options:</p>
          <div className="space-y-1">
            {suggestions.recommended_charts.slice(1).map((chart, index) => (
              <div key={index} className="text-xs text-blue-600">
                • {chart.chart_type}: {chart.reason}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};