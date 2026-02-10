import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import UploadedDataset
from .serializers import UploadedDatasetSerializer
import os

class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = UploadedDatasetSerializer(data=request.data)
        if file_serializer.is_valid():
            dataset = file_serializer.save()
            
            # Process the file
            try:
                file_path = dataset.file.path
                if not os.path.exists(file_path):
                     return Response({'error': 'File not saved correctly'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                df = pd.read_csv(file_path)

                # Expect columns: Equipment Name, Type, Flowrate, Pressure, Temperature
                # Calculate summary
                total_count = len(df)
                
                # Averages (numeric columns)
                numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
                averages = {}
                for col in numeric_cols:
                    if col in df.columns:
                         # Convert to float, coercing errors
                         df[col] = pd.to_numeric(df[col], errors='coerce')
                         averages[col] = df[col].mean()
                
                # Equipment Type Distribution
                type_distribution = {}
                averages_by_type = {}
                if 'Type' in df.columns:
                    type_distribution = df['Type'].value_counts().to_dict()
                    # Calculate averages per type
                    try:
                        grouped = df.groupby('Type')[numeric_cols].mean()
                        averages_by_type = grouped.to_dict(orient='index')
                    except Exception as e:
                        print(f"Error calculating grouped averages: {e}")

                summary = {
                    'total_count': total_count,
                    'averages': averages,
                    'averages_by_type': averages_by_type,
                    'type_distribution': type_distribution,
                    'preview': df.head().fillna('').to_dict(orient='records')
                }
                
                dataset.summary = summary
                dataset.save()
                
                return Response(UploadedDatasetSerializer(dataset).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                # If processing specific error, maybe keep the file for debugging? 
                # But typically we delete invalid uploads.
                dataset.delete()
                return Response({'error': f"Error processing file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoryView(APIView):
    def get(self, request):
        # Last 5 uploads
        datasets = UploadedDataset.objects.order_by('-uploaded_at')[:5]
        serializer = UploadedDatasetSerializer(datasets, many=True)
        return Response(serializer.data)
