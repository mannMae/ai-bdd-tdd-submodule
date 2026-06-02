import type { ReactNode } from 'react';
import React from 'react';
import { useForm } from 'react-hook-form';
import type { UseFormReturn, UseFormProps, FieldValues } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { ZodType } from 'zod';

type FormProps<TFormValues extends FieldValues, Schema> = {
  onSubmit: (values: TFormValues, methods: UseFormReturn<TFormValues>) => void;
  children: (methods: UseFormReturn<TFormValues>) => ReactNode;
  options?: UseFormProps<TFormValues>;
  id?: string;
  className?: string;
  schema: Schema;
};

export const Form = <
  Schema extends ZodType<any, any, any>,
  TFormValues extends FieldValues = any,
>({
  onSubmit,
  children,
  options,
  id,
  className,
  schema,
}: FormProps<TFormValues, Schema>) => {
  const methods = useForm<TFormValues>({
    ...options,
    resolver: zodResolver(schema),
  });

  return (
    <form
      onSubmit={methods.handleSubmit((values) => onSubmit(values, methods))}
      id={id}
      className={className}
    >
      {children(methods)}
    </form>
  );
};

export default Form;
