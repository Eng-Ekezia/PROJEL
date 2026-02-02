import { useParams, useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"

export default function ProjectDetails() {
  const { id } = useParams()
  const navigate = useNavigate()

  return (
    <div className="flex flex-col items-center justify-center h-[50vh] gap-4">
      <h1 className="text-2xl font-bold">Detalhes do Projeto: {id}</h1>
      <p className="text-muted-foreground">Esta tela está sendo migrada para o novo design.</p>
      <Button variant="outline" onClick={() => navigate("/")}>
        <ArrowLeft className="mr-2 h-4 w-4" /> Voltar para Dashboard
      </Button>
    </div>
  )
}