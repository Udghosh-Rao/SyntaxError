export interface Event {
  id: number;
  title: string;
  date: string;
  location: string;
  description: string;
  image: string;
  category: 'sports' | 'music' | 'tech';
  attendees: number;
  organizer_id: number;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  email: string;
  name: string;
  role: 'user' | 'organizer' | 'admin';
  created_at: string;
  updated_at: string;
}

export interface EventRegistration {
  id: number;
  event_id: number;
  user_id: number;
  registered_at: string;
  status: 'pending' | 'confirmed' | 'cancelled';
}

export interface ChatMessage {
  id: number;
  user_id: number;
  event_id: number;
  message: string;
  created_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}
