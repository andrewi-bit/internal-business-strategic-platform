export interface DivisionItem {
  id: string
  name: string
  code: string
}

export interface DivisionListResponse {
  success: boolean
  message: string
  data: DivisionItem[]
}
