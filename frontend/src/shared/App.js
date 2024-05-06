
export default function App({ children }) {
  return (
    <div
    className='h-screen w-screen overflow-x-hidden'
    style={{
      backgroundImage: `url("https://wallpaper.dog/large/10744114.jpg")`,
      backgroundSize: "cover"
    }}
    >
      {children}
    </div>
  );
}


