# ShadcnSkill Examples

Practical examples and walkthroughs for shadcn/ui integration in Next.js.

---

## Example 1: Complete shadcn/ui Setup

### Step-by-Step Walkthrough

```bash
# 1. Create Next.js project with Tailwind
npx create-next-app@latest my-app --typescript --tailwind --app

# 2. Navigate to project
cd my-app

# 3. Install shadcn/ui dependencies
npm install class-variance-authority clsx tailwind-merge
npm install @radix-ui/react-slot @radix-ui/react-dialog @radix-ui/react-dropdown-menu

# 4. Generate shadcn components
python .claude/skills/shadcn-skill/scripts/generate-components.py --output-dir ./app

# 5. Validate setup
python .claude/skills/shadcn-skill/scripts/validate-setup.py .

# 6. Run development server
npm run dev
```

---

## Example 2: Using Button Component

### Basic Button Usage

```typescript
// app/page.tsx
import { Button } from '@/components/Button'

export default function Home() {
  return (
    <div className="p-8 space-y-4">
      <h1 className="text-3xl font-bold mb-8">Button Examples</h1>

      {/* Variants */}
      <div className="flex gap-4">
        <Button variant="default">Default</Button>
        <Button variant="destructive">Destructive</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="link">Link</Button>
      </div>

      {/* Sizes */}
      <div className="flex gap-4 items-center">
        <Button size="sm">Small</Button>
        <Button size="default">Default</Button>
        <Button size="lg">Large</Button>
        <Button size="icon">
          <svg className="w-4 h-4" />
        </Button>
      </div>

      {/* States */}
      <div className="flex gap-4">
        <Button disabled>Disabled</Button>
        <Button>
          <span className="mr-2">Loading...</span>
        </Button>
      </div>
    </div>
  )
}
```

### Button with Form

```typescript
'use client'

import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { useState } from 'react'

export default function ContactForm() {
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    // Submit form
    setTimeout(() => setLoading(false), 2000)
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md space-y-4">
      <Input placeholder="Your name" required />
      <Input type="email" placeholder="Email" required />
      <Button type="submit" disabled={loading} className="w-full">
        {loading ? 'Sending...' : 'Send Message'}
      </Button>
    </form>
  )
}
```

---

## Example 3: Using Card Component

### Basic Card

```typescript
// app/dashboard/page.tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/Card'
import { Button } from '@/components/Button'

export default function Dashboard() {
  return (
    <div className="p-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Total Users</CardTitle>
            <CardDescription>Active users this month</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">2,543</p>
            <p className="text-sm text-green-600 mt-2">↑ 12% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Revenue</CardTitle>
            <CardDescription>Total revenue</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">$45,231</p>
            <p className="text-sm text-green-600 mt-2">↑ 8% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Conversions</CardTitle>
            <CardDescription>Conversion rate</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">3.2%</p>
            <p className="text-sm text-red-600 mt-2">↓ 2% from last month</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
```

### Card with Actions

```typescript
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/Card'
import { Button } from '@/components/Button'

export default function PricingCard() {
  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Pro Plan</CardTitle>
        <CardDescription>Perfect for professionals</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="text-4xl font-bold">
          $29<span className="text-lg text-muted-foreground">/month</span>
        </div>
        <ul className="mt-6 space-y-3 text-sm">
          <li className="flex items-center">
            <svg className="w-4 h-4 mr-2 text-green-500" />
            Unlimited projects
          </li>
          <li className="flex items-center">
            <svg className="w-4 h-4 mr-2 text-green-500" />
            Priority support
          </li>
          <li className="flex items-center">
            <svg className="w-4 h-4 mr-2 text-green-500" />
            Advanced analytics
          </li>
        </ul>
      </CardContent>
      <CardFooter>
        <Button className="w-full">Subscribe Now</Button>
      </CardFooter>
    </Card>
  )
}
```

---

## Example 4: Using Input Component

### Form with Inputs

```typescript
'use client'

import { Input } from '@/components/Input'
import { Button } from '@/components/Button'
import { useState } from 'react'

export default function SignupForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  return (
    <form className="max-w-md space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">Full Name</label>
        <Input
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="John Doe"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Email</label>
        <Input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="john@example.com"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Password</label>
        <Input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="••••••••"
          required
        />
      </div>

      <Button type="submit" className="w-full">
        Create Account
      </Button>
    </form>
  )
}
```

---

## Example 5: Using Modal (Dialog) Component

### Basic Modal

```typescript
'use client'

import { Button } from '@/components/Button'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/Modal'

export default function ModalExample() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Open Modal</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Welcome!</DialogTitle>
          <DialogDescription>
            This is a shadcn/ui dialog component built with Radix UI.
          </DialogDescription>
        </DialogHeader>
        <div className="py-4">
          <p className="text-sm text-muted-foreground">
            Click outside or press ESC to close.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  )
}
```

### Modal with useModal Hook

```typescript
'use client'

import { Button } from '@/components/Button'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/Modal'
import { useModal } from '@/hooks/useModal'

export default function DeleteConfirmation() {
  const { isOpen, openModal, closeModal } = useModal()

  const handleDelete = () => {
    // Perform delete action
    console.log('Item deleted')
    closeModal()
  }

  return (
    <>
      <Button variant="destructive" onClick={openModal}>
        Delete Item
      </Button>

      <Dialog open={isOpen} onOpenChange={closeModal}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Are you absolutely sure?</DialogTitle>
            <DialogDescription>
              This action cannot be undone. This will permanently delete your item.
            </DialogDescription>
          </DialogHeader>
          <div className="flex justify-end gap-3 mt-4">
            <Button variant="outline" onClick={closeModal}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete}>
              Delete
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}
```

---

## Example 6: Using Navbar Component

### Navbar in Layout

```typescript
// app/layout.tsx
import { Navbar } from '@/components/Navbar'
import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  )
}
```

### Page with Navbar

```typescript
// app/page.tsx
export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold">Welcome</h1>
      <p className="text-muted-foreground mt-4">
        This page includes the shadcn/ui Navbar component.
      </p>
    </div>
  )
}
```

---

## Example 7: Wrapping layout.tsx with shadcn Provider

### Complete Layout Setup

```typescript
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My App',
  description: 'Built with Next.js and shadcn/ui',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
```

### With Theme Provider

```typescript
// app/layout.tsx
'use client'

import { ThemeProvider } from 'next-themes'
import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

---

## Example 8: Complete Dashboard Example

```typescript
// app/dashboard/page.tsx
'use client'

import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/Card'
import { Button } from '@/components/Button'
import { Input } from '@/components/Input'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/Modal'
import { useState } from 'react'

export default function Dashboard() {
  const [searchTerm, setSearchTerm] = useState('')

  return (
    <div className="container mx-auto p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold">Dashboard</h1>

        <Dialog>
          <DialogTrigger asChild>
            <Button>Create New</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Item</DialogTitle>
              <DialogDescription>
                Fill in the details below to create a new item.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <Input placeholder="Item name" />
              <Input placeholder="Description" />
              <Button className="w-full">Create</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="mb-6">
        <Input
          placeholder="Search..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-md"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Project Alpha</CardTitle>
            <CardDescription>In Progress</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              75% complete
            </p>
            <div className="mt-4 flex gap-2">
              <Button size="sm" variant="outline">View</Button>
              <Button size="sm">Edit</Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Project Beta</CardTitle>
            <CardDescription>Planning</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              25% complete
            </p>
            <div className="mt-4 flex gap-2">
              <Button size="sm" variant="outline">View</Button>
              <Button size="sm">Edit</Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Project Gamma</CardTitle>
            <CardDescription>Completed</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              100% complete
            </p>
            <div className="mt-4 flex gap-2">
              <Button size="sm" variant="outline">View</Button>
              <Button size="sm" variant="ghost">Archive</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
```

---

**Skill**: ShadcnSkill
**Version**: 1.0.0
**Updated**: 2025-12-31
