const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:3333';

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`Erro na requisição: ${response.status}`);
  }

  return (await response.json()) as T;
}
