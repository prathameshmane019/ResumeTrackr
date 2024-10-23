'use client'

import { useState } from 'react'
import { ResumeUpload } from './components/resume-upload'
import { AnalysisResults } from './components/AnalysisResults'
import { ResumeHistory } from './components/resume-history'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function Home() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [resumeHistory, setResumeHistory] = useState([])

  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result)
    setResumeHistory(prevHistory => [...prevHistory, { ...result, date: new Date().toISOString() }])
  }

  return (
    <div className="container px-20 py-8 ">
      <h1 className="text-4xl font-bold mb-8 text-center">AI Resume Score Tracker</h1>
      
      <Tabs defaultValue="upload" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="upload">Upload Resume</TabsTrigger>
          <TabsTrigger value="results">Analysis Results</TabsTrigger>
          <TabsTrigger value="history">Resume History</TabsTrigger>
        </TabsList>
        <TabsContent value="upload">
          <ResumeUpload onAnalysisComplete={handleAnalysisComplete} />
        </TabsContent>
        <TabsContent value="results">
          <AnalysisResults result={analysisResult} />
        </TabsContent>
        <TabsContent value="history">
          <ResumeHistory history={resumeHistory} />
        </TabsContent>
      </Tabs>
    </div>
  )
}