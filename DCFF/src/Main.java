import java.util.*;



public class Main {
    public static void main(String[] args) {

        Double r;


        Scanner scanner = new Scanner(System.in);
        System.out.println("hány évre szeretné kiszámolni");

        int size = scanner.nextInt();

        System.out.println("addja meg az r értékét");

        r = scanner.nextDouble();

        ArrayList<Double> cf = new ArrayList<>();
        ArrayList<Long> DCFF = new ArrayList<>();

        for (Integer j = 0; j < size; j++) {

            System.out.println("adja meg a CF"+ (j + 1) + "-t");
            cf.add(scanner.nextDouble());

            Double numA = (cf.get(j));

            Double A = 1+r;
            Double numB = Math.pow(A, j);

            Long numC = Math.round(numA / numB);
            DCFF.add(j, numC);

            System.out.println(DCFF);

        }

        double sum = 0;
        for(Long d : DCFF){
            sum += d;
        }

        System.out.println(Math.round(sum));
        System.out.println("írja be a cég részvényeinek számát");
        int resveny = scanner.nextInt();
        System.out.println("DCFF: " + sum/resveny);
        }

    }
