"use client"

import { useState, useCallback } from "react"

export interface UseModalReturn {
  isOpen: boolean
  openModal: () => void
  closeModal: () => void
  toggleModal: () => void
}

export function useModal(defaultOpen: boolean = false): UseModalReturn {
  const [isOpen, setIsOpen] = useState(defaultOpen)

  const openModal = useCallback(() => {
    setIsOpen(true)
  }, [])

  const closeModal = useCallback(() => {
    setIsOpen(false)
  }, [])

  const toggleModal = useCallback(() => {
    setIsOpen((prev) => !prev)
  }, [])

  return {
    isOpen,
    openModal,
    closeModal,
    toggleModal,
  }
}
