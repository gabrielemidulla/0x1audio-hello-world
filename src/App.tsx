import { useState, type FormEvent } from "react"
import { host } from "@0x1audio/sdk/page"
import { Button, Card, CardContent, CardDescription, CardHeader, CardTitle, Input, Label } from "@0x1audio/design-system"

export function App() {
  const [name, setName] = useState("")
  const [message, setMessage] = useState("")
  const [pending, setPending] = useState(false)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const bridge = host()
    if (!bridge) {
      setMessage("Open this app in 0x1audio.")
      return
    }
    setPending(true)
    try {
      const result = await bridge.call<{ message: string }>("hello", { name })
      setMessage(result.message)
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Something went wrong.")
    } finally {
      setPending(false)
    }
  }

  return (
    <main className="grid min-h-svh place-items-center bg-background px-6 text-foreground">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>Hello</CardTitle>
          <CardDescription>Say hello through 0x1audio.</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="flex flex-col gap-4" onSubmit={(event) => void submit(event)}>
            <div className="flex flex-col gap-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                name="name"
                value={name}
                placeholder="Name"
                autoComplete="off"
                onChange={(event) => setName(event.target.value)}
              />
            </div>
            <Button type="submit" disabled={pending}>
              {pending ? "Hello…" : "Hello"}
            </Button>
            <p className="min-h-5 text-sm">{message}</p>
          </form>
        </CardContent>
      </Card>
    </main>
  )
}
