import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'

export function AnalysisResults({ result }) {
  const [activeTab, setActiveTab] = useState('overview')

  if (!result) return null

  const pieChartData = [
    { name: 'Match', value: result.keyword_match },
    { name: 'Gap', value: 100 - result.keyword_match },
  ]

  const COLORS = ['#4CAF50', '#FFA000']

  return (
    <Card>
      <CardHeader>
        <CardTitle>Analysis Results</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="details">Details</TabsTrigger>
            <TabsTrigger value="keywords">Keywords</TabsTrigger>
          </TabsList>
          <TabsContent value="overview">
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-2">Overall Score</h3>
                <Progress value={result.total_score} className="w-full" />
                <p className="text-sm text-muted-foreground mt-1">{result.total_score.toFixed(2)}%</p>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-2">Keyword Match</h3>
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie
                      data={pieChartData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      fill="#8884d8"
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {pieChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
                <p className="text-sm text-muted-foreground text-center mt-2">{result.keyword_match.toFixed(2)}% match</p>
              </div>
            </div>
          </TabsContent>
          <TabsContent value="details">
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-2">Strengths</h3>
                <ul className="list-disc pl-5 space-y-1">
                  {result.strengths.map((strength, index) => (
                    <li key={index} className="text-sm">{strength}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-2">Areas for Improvement</h3>
                <ul className="list-disc pl-5 space-y-1">
                  {result.weaknesses.map((weakness, index) => (
                    <li key={index} className="text-sm">{weakness}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-2">Suggestions</h3>
                <ul className="list-disc pl-5 space-y-1">
                  {result.suggestions.map((suggestion, index) => (
                    <li key={index} className="text-sm">{suggestion}</li>
                  ))}
                </ul>
              </div>
            </div>
          </TabsContent>
          <TabsContent value="keywords">
            <div>
              <h3 className="text-lg font-semibold mb-2">Matched Keywords</h3>
              <div className="grid grid-cols-2 gap-2">
                {result.matched_keywords.map((keyword, index) => (
                  <div key={index} className="text-sm">
                    <span className="font-medium">{keyword.keyword}</span>: {keyword.count}
                  </div>
                ))}
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}