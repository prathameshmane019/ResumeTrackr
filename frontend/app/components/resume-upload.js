'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Upload, Loader2, FileText } from 'lucide-react'
import { useToast } from "@/hooks/use-toast"

import { Progress } from '@/components/ui/progress'

export function ResumeUpload({ onAnalysisComplete }) {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const { toast } = useToast()

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      toast({
        title: 'File selected',
        description: `${selectedFile.name} has been selected for upload.`,
      })
    }
  }

  const handleUpload = async () => {
    if (!file) {
      toast({
        title: 'Error',
        description: 'Please select a file to upload.',
        variant: 'destructive',
      })
      return
    }

    setLoading(true)
    setUploadProgress(0)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('job_description', jobDescription)

    try {
      const response = await fetch('http://localhost:8000/analyze-resume', {
        method: 'POST',
        body: formData,
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          setUploadProgress(percentCompleted)
        },
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      const data = await response.json()
      console.log('Analysis result:', data)
      
      toast({
        title: 'Success',
        description: 'Resume analyzed successfully!',
      })
      
      onAnalysisComplete(data)
      
    } catch (error) {
      console.error('Upload failed:', error)
      toast({
        title: 'Error',
        description: 'Failed to analyze resume. Please try again.',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
      setUploadProgress(0)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Resume</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Resume</label>
            <div className="flex items-center space-x-2">
              <Input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
                className="hidden"
                id="resume-upload"
              />
              <label
                htmlFor="resume-upload"
                className="cursor-pointer bg-primary text-primary-foreground hover:bg-primary/90 inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 h-10 px-4 py-2"
              >
                <FileText className="mr-2 h-4 w-4" />
                Select File
              </label>
              {file && <span className="text-sm text-muted-foreground">{file.name}</span>}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Job Description</label>
            <Textarea
              placeholder="Paste job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={4}
            />
          </div>

          <Button
            onClick={handleUpload}
            className="w-full"
            disabled={!file || loading}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2  h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4" />
                Analyze Resume
              </>
            )}
          </Button>

          {uploadProgress > 0 && (
            <div>
              <Progress value={uploadProgress} className="w-full" />
              <p className="text-sm text-muted-foreground mt-1">{uploadProgress}% uploaded</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}