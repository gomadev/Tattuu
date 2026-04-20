interface SearchBarProps {
  value: string;
  placeholder: string;
  onChange: (value: string) => void;
}

export function SearchBar({ value, placeholder, onChange }: SearchBarProps) {
  return (
    <div className="search-wrap">
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="search-input"
      />
      <button type="button" className="filter-button" aria-label="Filtrar">
        Filtrar
      </button>
    </div>
  );
}
