import React from "react";

export default function LoadingSpinner({ message = "Loading data..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="w-10 h-10 border-4 border-brand-gray border-t-brand-gold rounded-full animate-spin" />
      <p className="mt-4 text-sm text-brand-light">{message}</p>
    </div>
  );
}
