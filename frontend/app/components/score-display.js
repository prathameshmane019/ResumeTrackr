'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const aiScoreData = [
  { date: '2024-01', score: 75, predictedScore: 80 },
  { date: '2024-02', score: 82, predictedScore: 85 },
  { date: '2024-03', score: 88, predictedScore: 90 },
  { date: '2024-04', score: 92, predictedScore: 95 },
  // Add more data
];

export function ScoreDisplay() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Resume Score History with AI Predictions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={aiScoreData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date"
                tickFormatter={(value) => {
                  const date = new Date(value);
                  return date.toLocaleDateString('default', { month: 'short', year: '2-digit' });
                }}
              />
              <YAxis 
                domain={[0, 100]}
                tickFormatter={(value) => `${value}%`}
              />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === 'predictedScore') return [`${value}%`, 'Predicted Score'];
                  return [`${value}%`, 'Score'];
                }}
                labelFormatter={(label) => {
                  const date = new Date(label);
                  return date.toLocaleDateString('default', { month: 'long', year: 'numeric' });
                }}
              />
              <Line 
                type="monotone" 
                dataKey="score" 
                stroke="#2563eb"
                strokeWidth={2}
                dot={{ fill: '#2563eb', strokeWidth: 2 }}
                activeDot={{ r: 6, fill: '#2563eb' }}
              />
              <Line 
                type="monotone" 
                dataKey="predictedScore" 
                stroke="#ff7300"
                strokeWidth={2}
                dot={{ fill: '#ff7300', strokeWidth: 2 }}
                activeDot={{ r: 6, fill: '#ff7300' }}
                strokeDasharray="5 5"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
