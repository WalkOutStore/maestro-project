import React, { createContext, useContext } from 'react';
import { toast } from 'sonner';

const NotificationContext = createContext();

export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};

export const NotificationProvider = ({ children }) => {
  const showSuccess = (message, options = {}) => {
    return toast.success(message, {
      duration: 4000,
      ...options,
    });
  };

  const showError = (message, options = {}) => {
    return toast.error(message, {
      duration: 5000,
      ...options,
    });
  };

  const showInfo = (message, options = {}) => {
    return toast.info(message, {
      duration: 4000,
      ...options,
    });
  };

  const showWarning = (message, options = {}) => {
    return toast.warning(message, {
      duration: 4000,
      ...options,
    });
  };

  const showLoading = (message, options = {}) => {
    return toast.loading(message, options);
  };

  const dismiss = (toastId) => {
    toast.dismiss(toastId);
  };

  const dismissAll = () => {
    toast.dismiss();
  };

  const value = {
    showSuccess,
    showError,
    showInfo,
    showWarning,
    showLoading,
    dismiss,
    dismissAll,
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
};
